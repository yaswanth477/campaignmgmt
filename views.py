from flask import render_template, request, redirect, flash, url_for, Response, stream_with_context, jsonify, json, make_response
from models import Campaign, Filters, Sorts, Dedups, Classifies, Classify_rules, Distributes, Distribute_rules,Minus, db
from cmpMgmtServices import app
from sqlalchemy import create_engine
import datetime

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

#get api to get the specific campaign and its corresponding rules
@app.route('/flagship/<int:campaign_id>', methods=['GET', 'POST'])
def list_json(campaign_id):
#Get campaign details from campaign table using the ID parameter from endpoint

    responseObject = {
        'status': 'fail',
        'message': 'Campaign does not exist'
    }
    try:
        reqCampaign = Campaign.query.filter_by(id=int(campaign_id)).first()
        if not reqCampaign:
            return make_response(jsonify(responseObject)), 404
        else:
            campaign = Campaign.query.get(campaign_id)

            #Array declration for rules
            campaign_filters = []
            campaign_sorts = []
            campaign_dedups = []
            campaign_classifies = []
            campaign_classify_rules = []

        #Get all corrsponding transformation rules for the campaign from components tables
            all_filters = Filters.query.filter_by(campaign_id=campaign_id).all()
            all_sorts = Sorts.query.filter_by(campaign_id=campaign_id).all()
            all_dedups = Dedups.query.filter_by(campaign_id=campaign_id).all()
            campaign_drop_dt = str(campaign.campaign_drop_dt)
            campaign_effective_dt = str(campaign.campaign_effective_dt)

        #create filter object with required key value pairs
            for all_filter in all_filters:
                filterObj = {
                    'filterName': all_filter.filter_column,
                    'filterOperator': all_filter.filter_operator,
                    'filterValue': all_filter.filter_value,
                    'ruleSequence': all_filter.rule_seq
                }
                campaign_filters.append(filterObj)

        #create sort object with required key value pairs
            for all_sort in all_sorts:
                sortObj = {
                    'sortKeys': all_sort.sort_keys,
                    'order': all_sort.order,
                    'ruleSequence': all_sort.rule_seq
                }
                campaign_sorts.append(sortObj)

        #create dedup object with required key value pairs
            for all_dedup in all_dedups:
                dedupObj = {
                    'dedupKeys': all_dedup.dedup_keys,
                    'retain': all_dedup.retain,
                    'ruleSequence': all_dedup.rule_seq
                }
                campaign_dedups.append(dedupObj)

        #create response object and include all component rules to the object
            campaignObj = {
                "campaignName" : campaign.campaign_name,
                "strategyNumber" : campaign.strategy_number,
                "MarketingChannel" : campaign.marketing_channel,
                "campaignDropDate": campaign_drop_dt,
                "campaignEffectiveDate": campaign_effective_dt,
                "eligiblePopulationType": campaign.eligible_population_type,
                "lineOfBusiness": campaign.line_of_business,
                "privacySuppressionIndicator": campaign.privacy_suppression_ind,
                "filters": campaign_filters,
                "sorts": campaign_sorts,
                "dedups": campaign_dedups
            }

            responseObject = {
                'status':'success',
                'data': campaignObj
            }
            return make_response(jsonify(campaignObj)), 200
    except ValueError:
        return make_response(jsonify(responseObject)), 400





#POST api to create new campaign
@app.route('/flagship/', methods=['POST'])
def create_campaign():
    if request.method == 'POST':
        responseObject = {
            'status': 'failed',
            'message': 'Campaign is not created'
        }
        responseObjectNotValidJson = {
            'status': 'failed',
            'message': 'Request is not a valid json object'
        }
        try:
            json_data = request.get_json(force=True)
            # json_object = json.loads(json_data)
            if not json_data.get('marketingChannel','campaignDropDate'):
                return make_response(jsonify(responseObjectNotValidJson)), 406
            else:
                json_data =request.get_json(force=True)

                #identify the eligible population
                if json_data.get('eligiblePopulationType') == 'MTG':
                    inpuFileUrl='s3://cof-sbx-fsda-cohl-npi-analytic/flagship/part-00000-a77e5e45-aef3-489e-be96-01a4ed3a1f71.snappy.parquet'
                elif json_data.get('eligiblePopulationType') == 'HE':
                    inpuFileUrl = 's3://url_to_HE_s3_file/file_name'
                elif json_data.get('eligiblePopulationType') == 'HE':
                    inpuFileUrl = 's3://url_to_CRA_s3_file/file_name'


                all_filters = json_data.get('filters')
                all_sorts = json_data.get('sorts')
                all_dedups = json_data.get('dedups')
                all_classifies = json_data.get('classifies')
                all_distributes = json_data.get('distributes')
                all_minus = json_data.get('minus')



                newCampaign = Campaign(
                   campaign_name = json_data.get('campaignName'),strategy_number = json_data.get('strategyNumber'),
                   marketing_channel = json_data.get('marketingChannel'),campaign_effective_dt = json_data.get('campaignEffectiveDate'),
                   campaign_drop_dt=json_data.get('campaignDropDate'),
                   input_file_url=inpuFileUrl,
                   input_file_type='parquet',
                   output_table_name=json_data.get('campaignName') + '_readFileOutput' + str(json_data.get('ruleSequence')),
                   eligible_population_type = json_data.get('eligiblePopulationType'),
                   line_of_business = json_data.get('lineOfBusiness'),
                   # privacy_suppression_ind = json_data.get('privacySuppressionIndicator'),
                   rule_seq = json_data.get('ruleSequence'),
                   inserted_dt = datetime.datetime.now().replace(second= 0, microsecond=0),
                   inserted_by = json_data.get('user'),
                   # updated_dt = datetime.datetime.now().replace(second= 0, microsecond=0),
                )

                db.session.add(newCampaign)

                if(all_filters):
                   input_table_name = json_data.get('campaignName') + '_readFileOutput' + str(json_data.get('ruleSequence'))
                   for filter in all_filters:
                       output_table_name = json_data.get('campaignName') + '_FilterOutput' + str(filter['ruleSequence'])
                       newFilter = Filters(
                           filter_column=filter['filterName'],filter_operator=filter['filterOperator'],
                           filter_value=filter['filterValue'],inserted_dt=datetime.datetime.now().replace(second= 0, microsecond=0),
                           input_table_name=input_table_name, output_table_name=output_table_name, rule_seq = filter['ruleSequence'],
                           inserted_by=json_data.get('user'),parent = newCampaign,
                       )
                       input_table_name=output_table_name
                       input_to_classify=output_table_name
                       db.session.add(newFilter)

                if(all_sorts):
                   for sort in all_sorts:
                       newSort = Sorts(
                           sort_keys=sort['sortKeys'],rule_seq=sort['ruleSequence'],
                           order=sort['order'],inserted_dt='2017-01-01',
                           inserted_by='yji914',updated_dt='2017-09-09',updated_by='yji914',parent = newCampaign
                       )
                       db.session.add(newSort)

                if(all_classifies):
                    input_table = input_to_classify
                    for classify in all_classifies:
                        output_table_classify = json_data.get('campaignName') + '_ClassifyOutput' + str(
                            classify['ruleSequence'])
                        newClassify = Classifies(
                            input_table_name=input_table,output_table_name=output_table_classify,
                            rule_seq=classify['ruleSequence'],inserted_dt=datetime.datetime.now().replace(second= 0, microsecond=0),
                            inserted_by=json_data.get('user'),parent = newCampaign
                        )
                        classify_rules = classify['classifyRules']
                        db.session.add(newClassify)
                        for each_rule in classify_rules:
                            newClassifyRules = Classify_rules(
                                expressions=each_rule['expressions'],
                                vendor_cell_value=each_rule['VendorCell'],
                                vendor_cell_description=each_rule['VendorDesc'],
                                classify_rule_order=each_rule['ruleNumber'], inserted_dt=datetime.datetime.now().replace(second= 0, microsecond=0),
                                inserted_by=json_data.get('user'),parent=newClassify
                            )
                            db.session.add(newClassifyRules)


                if (all_distributes):
                    input_table_distribute = output_table_classify
                    for distribute in all_distributes:
                        output_table_distribute = json_data.get('campaignName') + '_DistributeOutput' + str(
                            distribute['ruleSequence'])
                        newDistribute = Distributes(
                            input_table_name=input_table_distribute, output_table_name=output_table_distribute,
                            rule_seq=distribute['ruleSequence'],
                            inserted_dt=datetime.datetime.now().replace(second=0, microsecond=0),
                            inserted_by=json_data.get('user'), parent=newCampaign
                        )
                        distribute_rules = distribute['distributeRules']
                        db.session.add(newDistribute)
                        for each_rule in distribute_rules:
                            newDistributeRules = Distribute_rules(
                                expressions=each_rule['expressions'],
                                test_cell_weight=each_rule['testCellWeight'],
                                controlled_cell_weight=each_rule['controlCellWeight'],
                                distribute_rule_order=each_rule['ruleNumber'],
                                inserted_dt=datetime.datetime.now().replace(second=0, microsecond=0),
                                inserted_by=json_data.get('user'), parent=newDistribute
                            )
                            db.session.add(newDistributeRules)

                if(all_dedups):
                    for dedup in all_dedups:
                       output_table_dedup = json_data.get('campaignName') + '_DedupOutput' + str(
                            dedup['ruleSequence'])
                       newDedup = Dedups(
                           unique_fields=dedup['uniqueFields'],
                           rule_seq=dedup['ruleSequence'],
                           dedup_fields=dedup['dedupFields'],
                           dedup_function=dedup['dedupFunction'],
                           description=dedup['dedupDescription'],
                           input_table_name=output_table_distribute,
                           output_table_name=output_table_dedup,
                           inserted_dt=datetime.datetime.now().replace(second=0, microsecond=0),
                           inserted_by=json_data.get('user'),
                           parent=newCampaign
                       )
                       db.session.add(newDedup)

                if(all_minus):
                   calculate_minus_sequence = len(all_minus)
                   prev_table = output_table_dedup
                   for minus in all_minus:
                       output_table_read = json_data.get('campaignName') + '_ReadOutput' + str(
                           minus['ruleSequence']),
                       output_table_minus = json_data.get('campaignName') + '_MinusOutput' + str(
                           minus['ruleSequence'] + calculate_minus_sequence),
                       a=minus['ruleSequence']
                       newMinus= Minus(
                           s3input_table=minus['s3FileUrl'],
                           readfile_seq=minus['ruleSequence'],
                           minus_seq=minus['ruleSequence'] + calculate_minus_sequence,
                           input_table_name=prev_table,
                           read_table_output= output_table_read,
                           output_table_name=output_table_minus,
                           inserted_dt=datetime.datetime.now().replace(second=0, microsecond=0),
                           inserted_by=json_data.get('user'),
                           parent=newCampaign
                       )
                       prev_table = output_table_minus
                       db.session.add(newMinus)

                db.session.commit()

                responseObject = {
                    'status': 'success',
                    'data': "Campaign successfully created"
                }
                return make_response(jsonify(responseObject)), 200

        except ValueError:
            return make_response(jsonify(responseObject)), 406

import sys, json
from columnar import columnar # tabulating test results

def dump_test_results(test_results_list = [], log = None, event_detail = False) :
    pass

    names = []
    successes = []
    failing_tests = set()

    headers = ["PORT/PATH TESTED", "TEST", "RESULT(ACROSS ALL EVENTS)", "INFO"]
    if event_detail :
        headers = ["PORT/PATH TESTED", "EVENT L0ID", "TEST", "RESULT", "INFO"]
    rows = []

    for itest_result, test_results in enumerate(test_results_list) :
        test_results = test_results["test_results"]
        test_name = test_results["test_name"]
        overall_success = test_results["test_success"]
        names.append(test_name)
        successes.append(overall_success)

        sub_test_idx = 0
        results = test_results["results"]

        ##
        ## global
        ##
        global_results = results["global"]["RESULTS"]
        for test, test_info in global_results.items() :
            row_data = []

            ##
            ## fill the "PATH" column
            ##
            if sub_test_idx == 0 :
                row_data.append(test_name.replace("TEST_",""))
            else :
                row_data.append("")

            if event_detail :
                row_data.append("")

            row_data.append(test.upper())
            row_data.append( {True:"PASS",False:"FAIL"}[test_info[0]] )

            if not test_info[0] :
                failing_tests.add( test.upper() )

            if test_info[1] and event_detail :
                row_data.append( test_info[1] )
            else :
                row_data.append( "" )

            rows.append(row_data)
            sub_test_idx += 1

        ##
        ## event
        ##

        events = results["event"]

        filler_row = []
        filler_row.append("")
        for h in headers[1:-1] :
            filler_row.append( 10 * "//" )
        filler_row.append("")

        if event_detail :
            for ievent, event in enumerate(events) :
                if ievent > 0 :
                    rows.append(filler_row)
                l0id = event["L0ID"]
                event_results = event["RESULTS"]
                event_row = 0
                for test, test_info in event_results.items() :
                    row_data = []
        
                    ##
                    ## fill the "PATH" column
                    ##
                    if sub_test_idx == 0 :
                        row_data.append(test_name.replace("TEST_",""))
                    else :
                        row_data.append("")

                    if event_row == 0 :
                        row_data.append("{}".format(l0id))
                    else :
                        row_data.append("")
        
                    row_data.append(test.upper())
                    row_data.append( {True:"PASS",False:"FAIL"}[test_info[0]] )
                    if not test_info[0] :
                        failing_tests.add( test.upper() )

                    if test_info[1] :
                        row_data.append( test_info[1] )
                    else :
                        row_data.append( "" )
    
                    rows.append(row_data)
                    sub_test_idx += 1
                    event_row += 1

        else :
            test_names = []
            event_test_summary = {}
            bad_event_header_fields = set()
            bad_event_footer_fields = set()
            for ievent, event in enumerate(events) :
                event_results = event["RESULTS"]
                for test, test_info in event_results.items() :
                    if ievent == 0 :
                        test_names.append(test.upper())
                        event_test_summary[test.upper()] = True

                    if not test_info[0] :
                        failing_tests.add( test.upper() )
                        event_test_summary[test.upper()] = False
                        if "event_header" in test.lower() :
                            if "bad_fields" in test_info[1] :
                                for field in test_info[1]["bad_fields"] :
                                    bad_event_header_fields.add(field)
                        elif "event_footer" in test.lower() :
                            if "bad_fields" in test_info[1] :
                                for field in test_info[1]["bad_fields"] :
                                    bad_event_footer_fields.add(field)

            ##
            ## fill the "PATH" column
            ##

            for test in test_names :
                row_data = []

                if sub_test_idx == 0 :
                    row_data.append(test_name.replace("TEST_",""))
                else :
                    row_data.append("")

                row_data.append(test.upper())
                row_data.append( {True:"PASS",False:"FAIL"}[event_test_summary[test]] )
                if "event_header" in test.lower() and test_info[1] :
                    row_data.append( "bad_fields: {}".format(x for x in bad_event_header_fields) )
                elif "event_footer" in test.lower() :
                    bad_event_footer_fields = list(bad_event_footer_fields)
                    row_data.append( "bad_fields: {}".format([x for x in bad_event_footer_fields]))
                else :
                    row_data.append("")

                rows.append(row_data)
                sub_test_idx += 1

    table = columnar(rows, headers, no_borders = False)
    print(table)

def result_summary_dict(input0: str, input1: str, test_name: str, test_results: dict) -> dict :
    overall_passes = overall_test_result(test_results)
    out_results = {
        "test_results" :
        {
            "test_name" : test_name
            ,"test_success" : overall_passes
            ,"inputs" : {"input0" : input0, "input1" : input1}
            ,"results" : test_results
        }
    }
    return out_results

def overall_test_result(test_results: dict) -> bool :

    try :
        if "test_result" in test_results :
            results = test_results["test_results"]["results"]
        elif "results" in test_results :
            results = test_results["results"]
        else :
            if "global" in test_results and "event" in test_results :
                results = test_results
    except :
        raise Exception("ERROR Malformed test result dictionary provided")

    test_result = True # True = test passes, False = test fails
    ##
    ## global
    ##
    global_results = results["global"]
    if not global_results["TEST_RESULT"] :
        test_result = False

    ##
    ## event
    ##
    event_results = results["event"]
    for ievent, event_result_info in enumerate(event_results) :
        if not event_result_info["TEST_RESULT"] :
            test_result = False

    return test_result

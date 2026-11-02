/* ==============================================================================================
   TRANSACTIONAL FRAUD DETECTION ANALYSIS - POWER QUERY (M) ETL SCRIPTS
   Instructions:
   1. Open Power BI Desktop
   2. Click 'Get Data' -> 'Blank Query'
   3. Open 'Advanced Editor'
   4. Paste each query definition below into its respective query name
============================================================================================== */

// ==============================================================================================
// PARAMETER: DataDirectoryPath
// Update this path if the project folder is relocated
// ==============================================================================================
let
    DataDirectoryPath = "C:\Users\Aditya\Downloads\Infyntrex internship\Transactional Fraud Detection Analysis\PowerBI\data\" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
in
    DataDirectoryPath


// ==============================================================================================
// QUERY 1: Fact_Transactions
// Source: Fact_Transactions_Analytical.csv (or Fact_Transactions_Full.csv)
// ==============================================================================================
let
    Source = Csv.Document(File.Contents(DataDirectoryPath & "Fact_Transactions_Analytical.csv"), [Delimiter=",", Columns=41, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Transaction_ID", type text},
        {"Time", type number},
        {"Elapsed_Hours", type number},
        {"Hour_Of_Day", Int64.Type},
        {"Day_Window", type text},
        {"Time_Bucket", type text},
        {"Amount", type number},
        {"Amount_Band", type text},
        {"Class", Int64.Type},
        {"Fraud_Status", type text},
        {"Risk_Score", type number},
        {"Risk_Tier", type text},
        {"Predicted_Fraud", Int64.Type},
        {"V1", type number}, {"V2", type number}, {"V3", type number}, {"V4", type number},
        {"V5", type number}, {"V6", type number}, {"V7", type number}, {"V8", type number},
        {"V9", type number}, {"V10", type number}, {"V11", type number}, {"V12", type number},
        {"V13", type number}, {"V14", type number}, {"V15", type number}, {"V16", type number},
        {"V17", type number}, {"V18", type number}, {"V19", type number}, {"V20", type number},
        {"V21", type number}, {"V22", type number}, {"V23", type number}, {"V24", type number},
        {"V25", type number}, {"V26", type number}, {"V27", type number}, {"V28", type number}
    })
in
    #"Changed Type"


// ==============================================================================================
// QUERY 2: Dim_Time_Analysis
// Source: Dim_Time_Analysis.csv
// ==============================================================================================
let
    Source = Csv.Document(File.Contents(DataDirectoryPath & "Dim_Time_Analysis.csv"), [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Hour_Of_Day", Int64.Type},
        {"Hour_Label", type text},
        {"Time_Period", type text},
        {"Is_Vulnerability_Window", type text},
        {"Total_Transactions", Int64.Type},
        {"Fraud_Count", Int64.Type},
        {"Fraud_Rate_Pct", type number},
        {"Diurnal_Risk_Multiplier", type number},
        {"Total_Volume_USD", type number},
        {"Fraud_Loss_USD", type number},
        {"Recommended_Protocol", type text}
    })
in
    #"Changed Type"


// ==============================================================================================
// QUERY 3: Dim_Amount_Segments
// Source: Dim_Amount_Segments.csv
// ==============================================================================================
let
    Source = Csv.Document(File.Contents(DataDirectoryPath & "Dim_Amount_Segments.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Band_ID", Int64.Type},
        {"Band_Label", type text},
        {"Min_Amount", type number},
        {"Max_Amount", type number},
        {"Modus_Operandi", type text},
        {"Typical_Action", type text}
    })
in
    #"Changed Type"


// ==============================================================================================
// QUERY 4: Dim_Risk_Tiers
// Source: Dim_Risk_Tiers.csv
// ==============================================================================================
let
    Source = Csv.Document(File.Contents(DataDirectoryPath & "Dim_Risk_Tiers.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Tier_ID", Int64.Type},
        {"Tier_Name", type text},
        {"Risk_Min", type number},
        {"Risk_Max", type number},
        {"Policy_Action", type text},
        {"Coverage_Volume_Pct", type number},
        {"Customer_Friction", type text},
        {"False_Alarm_Risk", type text},
        {"SLA_Response", type text}
    })
in
    #"Changed Type"


// ==============================================================================================
// QUERY 5: Fact_Model_Benchmark
// Source: Fact_Model_Benchmark.csv
// ==============================================================================================
let
    Source = Csv.Document(File.Contents(DataDirectoryPath & "Fact_Model_Benchmark.csv"), [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Model_Name", type text},
        {"Architecture", type text},
        {"Accuracy_Pct", type number},
        {"Precision_Pct", type number},
        {"Recall_Catch_Rate_Pct", type number},
        {"F1_Score", type number},
        {"ROC_AUC", type number},
        {"PR_AUC", type number},
        {"Test_Sample_Size", Int64.Type},
        {"Actual_Frauds_In_Test", Int64.Type},
        {"True_Positives_Caught", Int64.Type},
        {"False_Positives_Alarms", Int64.Type},
        {"False_Negatives_Missed", Int64.Type},
        {"True_Negatives_Cleared", Int64.Type},
        {"False_Alarm_Ratio", type text},
        {"Direct_Fraud_Loss_Prevented_USD", type number},
        {"Manual_Review_Overhead_Hours", type number},
        {"Operational_Review_Cost_USD", type number},
        {"Net_Economic_Value_USD", type number},
        {"Verdict", type text}
    })
in
    #"Changed Type"


// ==============================================================================================
// QUERY 6: Dim_Feature_Drivers
// Source: Dim_Feature_Drivers.csv
// ==============================================================================================
let
    Source = Csv.Document(File.Contents(DataDirectoryPath & "Dim_Feature_Drivers.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Feature_Name", type text},
        {"Correlation_With_Fraud", type number},
        {"RF_Importance_Pct", type number},
        {"Indicator_Type", type text},
        {"Interpretation", type text}
    })
in
    #"Changed Type"


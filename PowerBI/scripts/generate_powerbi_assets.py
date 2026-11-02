"""
generate_powerbi_assets.py
Generates the complete Power BI Project (.pbip), Template (.pbit), model.bim, and report.json.
"""

import os
import sys
import json
import zipfile
from pathlib import Path

# Paths
base_dir = Path(r"C:\Users\Aditya\Downloads\Infyntrex internship\Transactional Fraud Detection Analysis")
pbi_dir = base_dir / "PowerBI"
data_dir = pbi_dir / "data"
semantic_dir = pbi_dir / "Transactional_Fraud_Detection_Dashboard.SemanticModel"
report_dir = pbi_dir / "Transactional_Fraud_Detection_Dashboard.Report"

semantic_dir.mkdir(parents=True, exist_ok=True)
report_dir.mkdir(parents=True, exist_ok=True)

# Normalized path with forward slashes for Power Query M
data_dir_str = str(data_dir).replace("\\", "/")

print("1. Generating definition.pbism...")
pbism_content = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
    "version": "4.2",
    "settings": {
        "qnaEnabled": True
    }
}
with open(semantic_dir / "definition.pbism", "w", encoding="utf-8") as f:
    json.dump(pbism_content, f, indent=2)

print("2. Generating definition.pbir...")
pbir_content = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/1.0.0/schema.json",
    "version": "4.0",
    "datasetReference": {
        "byPath": {
            "path": "../Transactional_Fraud_Detection_Dashboard.SemanticModel"
        },
        "byConnection": None
    }
}
with open(report_dir / "definition.pbir", "w", encoding="utf-8") as f:
    json.dump(pbir_content, f, indent=2)

print("3. Generating model.bim TMSL semantic model...")
model_bim = {
    "name": "Transactional_Fraud_Detection_SemanticModel",
    "compatibilityLevel": 1567,
    "model": {
        "culture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True
        },
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "en-US",
        "tables": [
            {
                "name": "Fact_Transactions",
                "columns": [
                    {"name": "Transaction_ID", "dataType": "string", "sourceColumn": "Transaction_ID"},
                    {"name": "Time", "dataType": "double", "sourceColumn": "Time"},
                    {"name": "Elapsed_Hours", "dataType": "double", "sourceColumn": "Elapsed_Hours"},
                    {"name": "Hour_Of_Day", "dataType": "int64", "sourceColumn": "Hour_Of_Day"},
                    {"name": "Day_Window", "dataType": "string", "sourceColumn": "Day_Window"},
                    {"name": "Time_Bucket", "dataType": "string", "sourceColumn": "Time_Bucket"},
                    {"name": "Amount", "dataType": "double", "sourceColumn": "Amount", "formatString": "$#,##0.00"},
                    {"name": "Amount_Band", "dataType": "string", "sourceColumn": "Amount_Band"},
                    {"name": "Class", "dataType": "int64", "sourceColumn": "Class"},
                    {"name": "Fraud_Status", "dataType": "string", "sourceColumn": "Fraud_Status"},
                    {"name": "Risk_Score", "dataType": "double", "sourceColumn": "Risk_Score", "formatString": "0.0000"},
                    {"name": "Risk_Tier", "dataType": "string", "sourceColumn": "Risk_Tier"},
                    {"name": "Predicted_Fraud", "dataType": "int64", "sourceColumn": "Predicted_Fraud"},
                    {"name": "V1", "dataType": "double", "sourceColumn": "V1"},
                    {"name": "V2", "dataType": "double", "sourceColumn": "V2"},
                    {"name": "V3", "dataType": "double", "sourceColumn": "V3"},
                    {"name": "V4", "dataType": "double", "sourceColumn": "V4"},
                    {"name": "V10", "dataType": "double", "sourceColumn": "V10"},
                    {"name": "V11", "dataType": "double", "sourceColumn": "V11"},
                    {"name": "V12", "dataType": "double", "sourceColumn": "V12"},
                    {"name": "V14", "dataType": "double", "sourceColumn": "V14"},
                    {"name": "V16", "dataType": "double", "sourceColumn": "V16"},
                    {"name": "V17", "dataType": "double", "sourceColumn": "V17"}
                ],
                "partitions": [
                    {
                        "name": "Fact_Transactions-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{data_dir_str}/Fact_Transactions_Analytical.csv"), [Delimiter=",", Columns=41, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{',
                                '        {"Transaction_ID", type text}, {"Time", type number}, {"Elapsed_Hours", type number},',
                                '        {"Hour_Of_Day", Int64.Type}, {"Day_Window", type text}, {"Time_Bucket", type text},',
                                '        {"Amount", type number}, {"Amount_Band", type text}, {"Class", Int64.Type},',
                                '        {"Fraud_Status", type text}, {"Risk_Score", type number}, {"Risk_Tier", type text},',
                                '        {"Predicted_Fraud", Int64.Type}, {"V14", type number}, {"V17", type number}, {"V12", type number}',
                                '    })',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ],
                "measures": [
                    {"name": "Total Transactions", "expression": "COUNTROWS(Fact_Transactions)"},
                    {"name": "Fraud Transactions", "expression": "CALCULATE(COUNTROWS(Fact_Transactions), Fact_Transactions[Class] = 1)"},
                    {"name": "Legitimate Transactions", "expression": "CALCULATE(COUNTROWS(Fact_Transactions), Fact_Transactions[Class] = 0)"},
                    {"name": "Fraud Rate %", "expression": "DIVIDE([Fraud Transactions], [Total Transactions], 0) * 100", "formatString": "0.000%"},
                    {"name": "Total Volume USD", "expression": "SUM(Fact_Transactions[Amount])", "formatString": "$#,##0.00"},
                    {"name": "Fraud Loss USD", "expression": "CALCULATE(SUM(Fact_Transactions[Amount]), Fact_Transactions[Class] = 1)", "formatString": "$#,##0.00"},
                    {"name": "Avg Transaction Amount", "expression": "AVERAGE(Fact_Transactions[Amount])", "formatString": "$#,##0.00"},
                    {"name": "Avg Fraud Amount", "expression": "CALCULATE(AVERAGE(Fact_Transactions[Amount]), Fact_Transactions[Class] = 1)", "formatString": "$#,##0.00"},
                    {"name": "Avg Legit Amount", "expression": "CALCULATE(AVERAGE(Fact_Transactions[Amount]), Fact_Transactions[Class] = 0)", "formatString": "$#,##0.00"},
                    {"name": "Nighttime Fraud Count", "expression": "CALCULATE([Fraud Transactions], Fact_Transactions[Hour_Of_Day] >= 0 && Fact_Transactions[Hour_Of_Day] <= 5)"},
                    {"name": "Nighttime Fraud Rate %", "expression": "DIVIDE([Nighttime Fraud Count], CALCULATE([Total Transactions], Fact_Transactions[Hour_Of_Day] >= 0 && Fact_Transactions[Hour_Of_Day] <= 5), 0) * 100", "formatString": "0.000%"},
                    {"name": "RF Fraud Catch Rate %", "expression": "81.63", "formatString": "0.00%"},
                    {"name": "RF Precision %", "expression": "75.47", "formatString": "0.00%"},
                    {"name": "False Alarm Reduction %", "expression": "98.26", "formatString": "0.00%"},
                    {"name": "Prevented Fraud Loss USD", "expression": "[Fraud Loss USD] * 0.8163", "formatString": "$#,##0.00"},
                    {"name": "Net Economic Value Delivered USD", "expression": "[Prevented Fraud Loss USD] + 73300", "formatString": "$#,##0.00"}
                ]
            },
            {
                "name": "Dim_Time_Analysis",
                "columns": [
                    {"name": "Hour_Of_Day", "dataType": "int64", "sourceColumn": "Hour_Of_Day"},
                    {"name": "Hour_Label", "dataType": "string", "sourceColumn": "Hour_Label"},
                    {"name": "Time_Period", "dataType": "string", "sourceColumn": "Time_Period"},
                    {"name": "Is_Vulnerability_Window", "dataType": "string", "sourceColumn": "Is_Vulnerability_Window"},
                    {"name": "Total_Transactions", "dataType": "int64", "sourceColumn": "Total_Transactions"},
                    {"name": "Fraud_Count", "dataType": "int64", "sourceColumn": "Fraud_Count"},
                    {"name": "Fraud_Rate_Pct", "dataType": "double", "sourceColumn": "Fraud_Rate_Pct", "formatString": "0.000%"},
                    {"name": "Diurnal_Risk_Multiplier", "dataType": "double", "sourceColumn": "Diurnal_Risk_Multiplier", "formatString": "0.0x"},
                    {"name": "Total_Volume_USD", "dataType": "double", "sourceColumn": "Total_Volume_USD", "formatString": "$#,##0.00"},
                    {"name": "Fraud_Loss_USD", "dataType": "double", "sourceColumn": "Fraud_Loss_USD", "formatString": "$#,##0.00"},
                    {"name": "Recommended_Protocol", "dataType": "string", "sourceColumn": "Recommended_Protocol"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Time_Analysis-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{data_dir_str}/Dim_Time_Analysis.csv"), [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{',
                                '        {"Hour_Of_Day", Int64.Type}, {"Hour_Label", type text}, {"Time_Period", type text},',
                                '        {"Is_Vulnerability_Window", type text}, {"Total_Transactions", Int64.Type}, {"Fraud_Count", Int64.Type},',
                                '        {"Fraud_Rate_Pct", type number}, {"Diurnal_Risk_Multiplier", type number}, {"Total_Volume_USD", type number},',
                                '        {"Fraud_Loss_USD", type number}, {"Recommended_Protocol", type text}',
                                '    })',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Dim_Amount_Segments",
                "columns": [
                    {"name": "Band_ID", "dataType": "int64", "sourceColumn": "Band_ID"},
                    {"name": "Band_Label", "dataType": "string", "sourceColumn": "Band_Label"},
                    {"name": "Min_Amount", "dataType": "double", "sourceColumn": "Min_Amount", "formatString": "$#,##0.00"},
                    {"name": "Max_Amount", "dataType": "double", "sourceColumn": "Max_Amount", "formatString": "$#,##0.00"},
                    {"name": "Modus_Operandi", "dataType": "string", "sourceColumn": "Modus_Operandi"},
                    {"name": "Typical_Action", "dataType": "string", "sourceColumn": "Typical_Action"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Amount_Segments-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{data_dir_str}/Dim_Amount_Segments.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{',
                                '        {"Band_ID", Int64.Type}, {"Band_Label", type text}, {"Min_Amount", type number},',
                                '        {"Max_Amount", type number}, {"Modus_Operandi", type text}, {"Typical_Action", type text}',
                                '    })',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Dim_Risk_Tiers",
                "columns": [
                    {"name": "Tier_ID", "dataType": "int64", "sourceColumn": "Tier_ID"},
                    {"name": "Tier_Name", "dataType": "string", "sourceColumn": "Tier_Name"},
                    {"name": "Risk_Min", "dataType": "double", "sourceColumn": "Risk_Min"},
                    {"name": "Risk_Max", "dataType": "double", "sourceColumn": "Risk_Max"},
                    {"name": "Policy_Action", "dataType": "string", "sourceColumn": "Policy_Action"},
                    {"name": "Coverage_Volume_Pct", "dataType": "double", "sourceColumn": "Coverage_Volume_Pct", "formatString": "0.00%"},
                    {"name": "Customer_Friction", "dataType": "string", "sourceColumn": "Customer_Friction"},
                    {"name": "False_Alarm_Risk", "dataType": "string", "sourceColumn": "False_Alarm_Risk"},
                    {"name": "SLA_Response", "dataType": "string", "sourceColumn": "SLA_Response"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Risk_Tiers-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{data_dir_str}/Dim_Risk_Tiers.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{',
                                '        {"Tier_ID", Int64.Type}, {"Tier_Name", type text}, {"Risk_Min", type number},',
                                '        {"Risk_Max", type number}, {"Policy_Action", type text}, {"Coverage_Volume_Pct", type number},',
                                '        {"Customer_Friction", type text}, {"False_Alarm_Risk", type text}, {"SLA_Response", type text}',
                                '    })',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Fact_Model_Benchmark",
                "columns": [
                    {"name": "Model_Name", "dataType": "string", "sourceColumn": "Model_Name"},
                    {"name": "Architecture", "dataType": "string", "sourceColumn": "Architecture"},
                    {"name": "Accuracy_Pct", "dataType": "double", "sourceColumn": "Accuracy_Pct", "formatString": "0.00%"},
                    {"name": "Precision_Pct", "dataType": "double", "sourceColumn": "Precision_Pct", "formatString": "0.00%"},
                    {"name": "Recall_Catch_Rate_Pct", "dataType": "double", "sourceColumn": "Recall_Catch_Rate_Pct", "formatString": "0.00%"},
                    {"name": "F1_Score", "dataType": "double", "sourceColumn": "F1_Score", "formatString": "0.0000"},
                    {"name": "ROC_AUC", "dataType": "double", "sourceColumn": "ROC_AUC", "formatString": "0.0000"},
                    {"name": "PR_AUC", "dataType": "double", "sourceColumn": "PR_AUC", "formatString": "0.0000"},
                    {"name": "Test_Sample_Size", "dataType": "int64", "sourceColumn": "Test_Sample_Size"},
                    {"name": "Actual_Frauds_In_Test", "dataType": "int64", "sourceColumn": "Actual_Frauds_In_Test"},
                    {"name": "True_Positives_Caught", "dataType": "int64", "sourceColumn": "True_Positives_Caught"},
                    {"name": "False_Positives_Alarms", "dataType": "int64", "sourceColumn": "False_Positives_Alarms"},
                    {"name": "False_Negatives_Missed", "dataType": "int64", "sourceColumn": "False_Negatives_Missed"},
                    {"name": "True_Negatives_Cleared", "dataType": "int64", "sourceColumn": "True_Negatives_Cleared"},
                    {"name": "False_Alarm_Ratio", "dataType": "string", "sourceColumn": "False_Alarm_Ratio"},
                    {"name": "Direct_Fraud_Loss_Prevented_USD", "dataType": "double", "sourceColumn": "Direct_Fraud_Loss_Prevented_USD", "formatString": "$#,##0.00"},
                    {"name": "Manual_Review_Overhead_Hours", "dataType": "double", "sourceColumn": "Manual_Review_Overhead_Hours", "formatString": "#,##0.0 hrs"},
                    {"name": "Operational_Review_Cost_USD", "dataType": "double", "sourceColumn": "Operational_Review_Cost_USD", "formatString": "$#,##0.00"},
                    {"name": "Net_Economic_Value_USD", "dataType": "double", "sourceColumn": "Net_Economic_Value_USD", "formatString": "$#,##0.00"},
                    {"name": "Verdict", "dataType": "string", "sourceColumn": "Verdict"}
                ],
                "partitions": [
                    {
                        "name": "Fact_Model_Benchmark-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{data_dir_str}/Fact_Model_Benchmark.csv"), [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{',
                                '        {"Model_Name", type text}, {"Architecture", type text}, {"Accuracy_Pct", type number},',
                                '        {"Precision_Pct", type number}, {"Recall_Catch_Rate_Pct", type number}, {"F1_Score", type number},',
                                '        {"ROC_AUC", type number}, {"PR_AUC", type number}, {"Test_Sample_Size", Int64.Type},',
                                '        {"Actual_Frauds_In_Test", Int64.Type}, {"True_Positives_Caught", Int64.Type},',
                                '        {"False_Positives_Alarms", Int64.Type}, {"False_Negatives_Missed", Int64.Type},',
                                '        {"True_Negatives_Cleared", Int64.Type}, {"False_Alarm_Ratio", type text},',
                                '        {"Direct_Fraud_Loss_Prevented_USD", type number}, {"Manual_Review_Overhead_Hours", type number},',
                                '        {"Operational_Review_Cost_USD", type number}, {"Net_Economic_Value_USD", type number},',
                                '        {"Verdict", type text}',
                                '    })',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Dim_Feature_Drivers",
                "columns": [
                    {"name": "Feature_Name", "dataType": "string", "sourceColumn": "Feature_Name"},
                    {"name": "Correlation_With_Fraud", "dataType": "double", "sourceColumn": "Correlation_With_Fraud", "formatString": "+0.0000;-0.0000;0.0000"},
                    {"name": "RF_Importance_Pct", "dataType": "double", "sourceColumn": "RF_Importance_Pct", "formatString": "0.0%"},
                    {"name": "Indicator_Type", "dataType": "string", "sourceColumn": "Indicator_Type"},
                    {"name": "Interpretation", "dataType": "string", "sourceColumn": "Interpretation"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Feature_Drivers-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{data_dir_str}/Dim_Feature_Drivers.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{',
                                '        {"Feature_Name", type text}, {"Correlation_With_Fraud", type number}, {"RF_Importance_Pct", type number},',
                                '        {"Indicator_Type", type text}, {"Interpretation", type text}',
                                '    })',
                                'in',
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ]
            }
        ],
        "relationships": [
            {
                "name": "Rel_Fact_DimTime",
                "fromTable": "Fact_Transactions",
                "fromColumn": "Hour_Of_Day",
                "toTable": "Dim_Time_Analysis",
                "toColumn": "Hour_Of_Day"
            },
            {
                "name": "Rel_Fact_DimAmount",
                "fromTable": "Fact_Transactions",
                "fromColumn": "Amount_Band",
                "toTable": "Dim_Amount_Segments",
                "toColumn": "Band_Label"
            },
            {
                "name": "Rel_Fact_DimTier",
                "fromTable": "Fact_Transactions",
                "fromColumn": "Risk_Tier",
                "toTable": "Dim_Risk_Tiers",
                "toColumn": "Tier_Name"
            }
        ]
    }
}

with open(semantic_dir / "model.bim", "w", encoding="utf-8") as f:
    json.dump(model_bim, f, indent=2)

print("4. Generating report.json for Power BI Report...")
# Professional executive layout structure
report_json = {
    "config": json.dumps({
        "version": "5.53",
        "themeCollection": {
            "baseTheme": {
                "name": "User",
                "version": "1.0",
                "type": 2
            }
        },
        "activeSectionIndex": 0,
        "defaultDrillFilterOtherVisuals": True
    }),
    "layoutOptimization": 0,
    "sections": [
        {
            "name": "ReportSection_ExecOverview",
            "displayName": "1. Executive KPI Overview",
            "filters": "[]",
            "ordinal": 0,
            "width": 1280.0,
            "height": 720.0,
            "config": json.dumps({
                "objects": {
                    "background": [{"properties": {"color": {"solid": {"color": "#0F172A"}}, "transparency": 0}}],
                    "outspace": [{"properties": {"color": {"solid": {"color": "#0B1120"}}, "transparency": 0}}]
                }
            }),
            "visualContainers": [
                # Title Ribbon
                {
                    "x": 20.0, "y": 15.0, "z": 1000.0, "width": 1240.0, "height": 65.0,
                    "config": json.dumps({
                        "name": "header_ribbon",
                        "singleVisual": {
                            "visualType": "textbox",
                            "objects": {
                                "general": [{"properties": {"paragraphs": [
                                    {"textRuns": [{"value": "TRANSACTIONAL FRAUD DETECTION & RISK INTELLIGENCE DASHBOARD", "textStyle": {"fontWeight": "bold", "fontSize": "16pt", "color": "#F8FAFC"}}]},
                                    {"textRuns": [{"value": "Infyntrex Internship | Portfolio Volume: $25.16M | 284,807 Transactions | Production Champion: Random Forest (+98.3% False Alarm Reduction)", "textStyle": {"fontSize": "9.5pt", "color": "#94A3B8"}}]}
                                ]}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # KPI Card 1: Total Portfolio Volume
                {
                    "x": 20.0, "y": 90.0, "z": 2000.0, "width": 195.0, "height": 95.0,
                    "config": json.dumps({
                        "name": "kpi_total_volume",
                        "singleVisual": {
                            "visualType": "card",
                            "projections": {"Values": [{"queryRef": "Fact_Transactions.Total Volume USD"}]},
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "TOTAL PORTFOLIO VOLUME", "fontSize": 9, "fontColor": {"solid": {"color": "#94A3B8"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#2563EB"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # KPI Card 2: Total Fraud Loss
                {
                    "x": 225.0, "y": 90.0, "z": 2001.0, "width": 195.0, "height": 95.0,
                    "config": json.dumps({
                        "name": "kpi_fraud_loss",
                        "singleVisual": {
                            "visualType": "card",
                            "projections": {"Values": [{"queryRef": "Fact_Transactions.Fraud Loss USD"}]},
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "TOTAL FRAUD EXPOSURE", "fontSize": 9, "fontColor": {"solid": {"color": "#EF4444"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#EF4444"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # KPI Card 3: Fraud Incidence Rate
                {
                    "x": 430.0, "y": 90.0, "z": 2002.0, "width": 195.0, "height": 95.0,
                    "config": json.dumps({
                        "name": "kpi_fraud_rate",
                        "singleVisual": {
                            "visualType": "card",
                            "projections": {"Values": [{"queryRef": "Fact_Transactions.Fraud Rate %"}]},
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "FRAUD RATE % (1 in 578)", "fontSize": 9, "fontColor": {"solid": {"color": "#94A3B8"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#F59E0B"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # KPI Card 4: Production Catch Rate
                {
                    "x": 635.0, "y": 90.0, "z": 2003.0, "width": 195.0, "height": 95.0,
                    "config": json.dumps({
                        "name": "kpi_catch_rate",
                        "singleVisual": {
                            "visualType": "card",
                            "projections": {"Values": [{"queryRef": "Fact_Transactions.RF Fraud Catch Rate %"}]},
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "RF FRAUD CATCH RATE", "fontSize": 9, "fontColor": {"solid": {"color": "#10B981"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#10B981"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # KPI Card 5: False Alarm Reduction
                {
                    "x": 840.0, "y": 90.0, "z": 2004.0, "width": 200.0, "height": 95.0,
                    "config": json.dumps({
                        "name": "kpi_false_alarm_red",
                        "singleVisual": {
                            "visualType": "card",
                            "projections": {"Values": [{"queryRef": "Fact_Transactions.False Alarm Reduction %"}]},
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "FALSE ALARM REDUCTION", "fontSize": 9, "fontColor": {"solid": {"color": "#06B6D4"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#06B6D4"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # KPI Card 6: Net Economic ROI
                {
                    "x": 1050.0, "y": 90.0, "z": 2005.0, "width": 210.0, "height": 95.0,
                    "config": json.dumps({
                        "name": "kpi_net_roi",
                        "singleVisual": {
                            "visualType": "card",
                            "projections": {"Values": [{"queryRef": "Fact_Transactions.Net Economic Value Delivered USD"}]},
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "NET VALUE GENERATED", "fontSize": 9, "fontColor": {"solid": {"color": "#10B981"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#10B981"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Visual: 24-Hour Diurnal Vulnerability Curve
                {
                    "x": 20.0, "y": 195.0, "z": 3000.0, "width": 780.0, "height": 260.0,
                    "config": json.dumps({
                        "name": "chart_diurnal_trend",
                        "singleVisual": {
                            "visualType": "lineChart",
                            "projections": {
                                "Category": [{"queryRef": "Dim_Time_Analysis.Hour_Of_Day"}],
                                "Y": [{"queryRef": "Dim_Time_Analysis.Fraud_Rate_Pct"}]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "DIURNAL VULNERABILITY: 2:00 AM SURGE (1.71% vs 0.17% Baseline - ~10x Spike)", "fontSize": 11, "fontColor": {"solid": {"color": "#F8FAFC"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Visual: Monetary Segment Breakdown
                {
                    "x": 810.0, "y": 195.0, "z": 3001.0, "width": 450.0, "height": 260.0,
                    "config": json.dumps({
                        "name": "chart_amount_distribution",
                        "singleVisual": {
                            "visualType": "barChart",
                            "projections": {
                                "Category": [{"queryRef": "Dim_Amount_Segments.Band_Label"}],
                                "Y": [{"queryRef": "Fact_Transactions.Fraud Loss USD"}]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "FRAUD LOSS BY AMOUNT TIER (Micro-Probing vs High-Value)", "fontSize": 11, "fontColor": {"solid": {"color": "#F8FAFC"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Visual: Model Benchmark Table
                {
                    "x": 20.0, "y": 465.0, "z": 4000.0, "width": 840.0, "height": 240.0,
                    "config": json.dumps({
                        "name": "table_model_benchmark",
                        "singleVisual": {
                            "visualType": "tableEx",
                            "projections": {
                                "Values": [
                                    {"queryRef": "Fact_Model_Benchmark.Model_Name"},
                                    {"queryRef": "Fact_Model_Benchmark.Precision_Pct"},
                                    {"queryRef": "Fact_Model_Benchmark.Recall_Catch_Rate_Pct"},
                                    {"queryRef": "Fact_Model_Benchmark.False_Positives_Alarms"},
                                    {"queryRef": "Fact_Model_Benchmark.Direct_Fraud_Loss_Prevented_USD"},
                                    {"queryRef": "Fact_Model_Benchmark.Net_Economic_Value_USD"}
                                ]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "MODEL PERFORMANCE & OPERATIONAL COST-BENEFIT BENCHMARK", "fontSize": 11, "fontColor": {"solid": {"color": "#F8FAFC"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Visual: Slicer - Time Window
                {
                    "x": 870.0, "y": 465.0, "z": 4001.0, "width": 390.0, "height": 240.0,
                    "config": json.dumps({
                        "name": "slicer_time_window",
                        "singleVisual": {
                            "visualType": "slicer",
                            "projections": {
                                "Values": [{"queryRef": "Fact_Transactions.Time_Bucket"}]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "INTERACTIVE FILTER: DIURNAL TIME WINDOW", "fontSize": 10, "fontColor": {"solid": {"color": "#94A3B8"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                }
            ]
        },
        # Page 2: Forensics & Diurnal Dynamics
        {
            "name": "ReportSection_Forensics",
            "displayName": "2. Fraud Pattern Forensics",
            "filters": "[]",
            "ordinal": 1,
            "width": 1280.0,
            "height": 720.0,
            "config": json.dumps({
                "objects": {
                    "background": [{"properties": {"color": {"solid": {"color": "#0F172A"}}, "transparency": 0}}],
                    "outspace": [{"properties": {"color": {"solid": {"color": "#0B1120"}}, "transparency": 0}}]
                }
            }),
            "visualContainers": [
                # Forensic Header
                {
                    "x": 20.0, "y": 15.0, "z": 1000.0, "width": 1240.0, "height": 55.0,
                    "config": json.dumps({
                        "name": "forensic_header",
                        "singleVisual": {
                            "visualType": "textbox",
                            "objects": {
                                "general": [{"properties": {"paragraphs": [
                                    {"textRuns": [{"value": "DEEP-DIVE FRAUD FORENSICS: MONETARY DYNAMICS & DIURNAL VULNERABILITY", "textStyle": {"fontWeight": "bold", "fontSize": "15pt", "color": "#F8FAFC"}}]},
                                    {"textRuns": [{"value": "Empirical evidence reveals dual fraud modalities: Micro Card Probing (<$5) and High-Value Extraction ($500+) during 02:00 AM vulnerability surge.", "textStyle": {"fontSize": "9pt", "color": "#94A3B8"}}]}
                                ]}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Hourly Forensics Bar & Line Combo
                {
                    "x": 20.0, "y": 80.0, "z": 2000.0, "width": 750.0, "height": 340.0,
                    "config": json.dumps({
                        "name": "hourly_forensics_chart",
                        "singleVisual": {
                            "visualType": "lineStackedColumnComboChart",
                            "projections": {
                                "Category": [{"queryRef": "Dim_Time_Analysis.Hour_Label"}],
                                "Y": [{"queryRef": "Dim_Time_Analysis.Fraud_Count"}],
                                "Y2": [{"queryRef": "Dim_Time_Analysis.Diurnal_Risk_Multiplier"}]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "HOURLY FRAUD INCIDENCE & RISK MULTIPLIER (PEAK: 2:00 AM AT 9.9x RISK)", "fontSize": 11, "fontColor": {"solid": {"color": "#F8FAFC"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Latent Feature Discriminators Bar
                {
                    "x": 780.0, "y": 80.0, "z": 2001.0, "width": 480.0, "height": 340.0,
                    "config": json.dumps({
                        "name": "feature_driver_chart",
                        "singleVisual": {
                            "visualType": "barChart",
                            "projections": {
                                "Category": [{"queryRef": "Dim_Feature_Drivers.Feature_Name"}],
                                "Y": [{"queryRef": "Dim_Feature_Drivers.RF_Importance_Pct"}]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "TOP PREDICTIVE FEATURE IMPORTANCE (V17, V14, V12 AS CORE ANCHORS)", "fontSize": 11, "fontColor": {"solid": {"color": "#F8FAFC"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Forensic Detail Table
                {
                    "x": 20.0, "y": 430.0, "z": 3000.0, "width": 1240.0, "height": 275.0,
                    "config": json.dumps({
                        "name": "forensic_details_table",
                        "singleVisual": {
                            "visualType": "tableEx",
                            "projections": {
                                "Values": [
                                    {"queryRef": "Dim_Time_Analysis.Hour_Label"},
                                    {"queryRef": "Dim_Time_Analysis.Time_Period"},
                                    {"queryRef": "Dim_Time_Analysis.Is_Vulnerability_Window"},
                                    {"queryRef": "Dim_Time_Analysis.Total_Transactions"},
                                    {"queryRef": "Dim_Time_Analysis.Fraud_Count"},
                                    {"queryRef": "Dim_Time_Analysis.Fraud_Rate_Pct"},
                                    {"queryRef": "Dim_Time_Analysis.Diurnal_Risk_Multiplier"},
                                    {"queryRef": "Dim_Time_Analysis.Fraud_Loss_USD"},
                                    {"queryRef": "Dim_Time_Analysis.Recommended_Protocol"}
                                ]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "24-HOUR FORENSIC AUDIT TABLE & RECOMMENDED OPERATIONAL SENSITIVITY", "fontSize": 11, "fontColor": {"solid": {"color": "#F8FAFC"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                }
            ]
        },
        # Page 3: ML Model Benchmark & Operational Efficiency
        {
            "name": "ReportSection_MLBenchmark",
            "displayName": "3. ML Benchmark & False Alarm ROI",
            "filters": "[]",
            "ordinal": 2,
            "width": 1280.0,
            "height": 720.0,
            "config": json.dumps({
                "objects": {
                    "background": [{"properties": {"color": {"solid": {"color": "#0F172A"}}, "transparency": 0}}],
                    "outspace": [{"properties": {"color": {"solid": {"color": "#0B1120"}}, "transparency": 0}}]
                }
            }),
            "visualContainers": [
                # ML Header
                {
                    "x": 20.0, "y": 15.0, "z": 1000.0, "width": 1240.0, "height": 55.0,
                    "config": json.dumps({
                        "name": "ml_header",
                        "singleVisual": {
                            "visualType": "textbox",
                            "objects": {
                                "general": [{"properties": {"paragraphs": [
                                    {"textRuns": [{"value": "MACHINE LEARNING BENCHMARK: RESOLVING INVESTIGATOR FATIGUE", "textStyle": {"fontWeight": "bold", "fontSize": "15pt", "color": "#F8FAFC"}}]},
                                    {"textRuns": [{"value": "While Logistic Regression catches 90.8% of frauds, it burns 1,492 false alarms. Random Forest slashes false alarms by 98.3% (down to 26), unlocking $47.8k in net economic value.", "textStyle": {"fontSize": "9pt", "color": "#94A3B8"}}]}
                                ]}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Confusion Matrix Card LR
                {
                    "x": 20.0, "y": 80.0, "z": 2000.0, "width": 395.0, "height": 330.0,
                    "config": json.dumps({
                        "name": "cm_lr_card",
                        "singleVisual": {
                            "visualType": "textbox",
                            "objects": {
                                "general": [{"properties": {"paragraphs": [
                                    {"textRuns": [{"value": "BASELINE: LOGISTIC REGRESSION", "textStyle": {"fontWeight": "bold", "fontSize": "12pt", "color": "#F59E0B"}}]},
                                    {"textRuns": [{"value": "\n\n• Test Corpus: 56,962 transactions (98 Frauds)", "textStyle": {"fontSize": "9.5pt", "color": "#E2E8F0"}}]},
                                    {"textRuns": [{"value": "\n• True Positives (Caught): 89 / 98 (90.82%)", "textStyle": {"fontSize": "9.5pt", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n• Missed Frauds (FN): 9 / 98 (9.18%)", "textStyle": {"fontSize": "9.5pt", "color": "#EF4444"}}]},
                                    {"textRuns": [{"value": "\n• False Alarms (FP): 1,492 transactions", "textStyle": {"fontSize": "10.5pt", "fontWeight": "bold", "color": "#EF4444"}}]},
                                    {"textRuns": [{"value": "\n• Precision: 5.63% (17 False Alarms per Fraud)", "textStyle": {"fontSize": "9.5pt", "color": "#EF4444"}}]},
                                    {"textRuns": [{"value": "\n• Review Overhead: 373 Analyst Hours", "textStyle": {"fontSize": "9.5pt", "color": "#94A3B8"}}]},
                                    {"textRuns": [{"value": "\n• Net Value: -$19,991 (Negative ROI)", "textStyle": {"fontSize": "10pt", "fontWeight": "bold", "color": "#EF4444"}}]}
                                ]}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#EF4444"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Confusion Matrix Card RF
                {
                    "x": 425.0, "y": 80.0, "z": 2001.0, "width": 395.0, "height": 330.0,
                    "config": json.dumps({
                        "name": "cm_rf_card",
                        "singleVisual": {
                            "visualType": "textbox",
                            "objects": {
                                "general": [{"properties": {"paragraphs": [
                                    {"textRuns": [{"value": "PRODUCTION CHAMPION: RANDOM FOREST", "textStyle": {"fontWeight": "bold", "fontSize": "12pt", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n\n• Test Corpus: 56,962 transactions (98 Frauds)", "textStyle": {"fontSize": "9.5pt", "color": "#E2E8F0"}}]},
                                    {"textRuns": [{"value": "\n• True Positives (Caught): 80 / 98 (81.63%)", "textStyle": {"fontSize": "9.5pt", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n• Missed Frauds (FN): 18 / 98 (18.37%)", "textStyle": {"fontSize": "9.5pt", "color": "#F59E0B"}}]},
                                    {"textRuns": [{"value": "\n• False Alarms (FP): 26 transactions (-98.3%)", "textStyle": {"fontSize": "10.5pt", "fontWeight": "bold", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n• Precision: 75.47% (0.3 False Alarms per Fraud)", "textStyle": {"fontSize": "9.5pt", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n• Review Overhead: 6.5 Analyst Hours", "textStyle": {"fontSize": "9.5pt", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n• Net Value: +$47,782 (Optimal ROI)", "textStyle": {"fontSize": "10pt", "fontWeight": "bold", "color": "#10B981"}}]}
                                ]}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#10B981"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # False Alarm Comparison Bar Chart
                {
                    "x": 830.0, "y": 80.0, "z": 2002.0, "width": 430.0, "height": 330.0,
                    "config": json.dumps({
                        "name": "chart_false_alarm_comparison",
                        "singleVisual": {
                            "visualType": "columnChart",
                            "projections": {
                                "Category": [{"queryRef": "Fact_Model_Benchmark.Model_Name"}],
                                "Y": [{"queryRef": "Fact_Model_Benchmark.False_Positives_Alarms"}]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "INVESTIGATION OVERHEAD: 1,492 vs 26 FALSE ALARMS", "fontSize": 11, "fontColor": {"solid": {"color": "#F8FAFC"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Model Tradeoff Summary Matrix
                {
                    "x": 20.0, "y": 420.0, "z": 3000.0, "width": 1240.0, "height": 285.0,
                    "config": json.dumps({
                        "name": "model_tradeoff_matrix",
                        "singleVisual": {
                            "visualType": "tableEx",
                            "projections": {
                                "Values": [
                                    {"queryRef": "Fact_Model_Benchmark.Model_Name"},
                                    {"queryRef": "Fact_Model_Benchmark.Architecture"},
                                    {"queryRef": "Fact_Model_Benchmark.Accuracy_Pct"},
                                    {"queryRef": "Fact_Model_Benchmark.Precision_Pct"},
                                    {"queryRef": "Fact_Model_Benchmark.Recall_Catch_Rate_Pct"},
                                    {"queryRef": "Fact_Model_Benchmark.PR_AUC"},
                                    {"queryRef": "Fact_Model_Benchmark.False_Positives_Alarms"},
                                    {"queryRef": "Fact_Model_Benchmark.False_Alarm_Ratio"},
                                    {"queryRef": "Fact_Model_Benchmark.Net_Economic_Value_USD"},
                                    {"queryRef": "Fact_Model_Benchmark.Verdict"}
                                ]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "EXECUTIVE ARCHITECTURE SCORECARD & DEPLOYMENT VERDICT", "fontSize": 11, "fontColor": {"solid": {"color": "#F8FAFC"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                }
            ]
        },
        # Page 4: Strategic 3-Tier Mitigation Engine
        {
            "name": "ReportSection_StrategicEngine",
            "displayName": "4. Strategic 3-Tier Mitigation Engine",
            "filters": "[]",
            "ordinal": 3,
            "width": 1280.0,
            "height": 720.0,
            "config": json.dumps({
                "objects": {
                    "background": [{"properties": {"color": {"solid": {"color": "#0F172A"}}, "transparency": 0}}],
                    "outspace": [{"properties": {"color": {"solid": {"color": "#0B1120"}}, "transparency": 0}}]
                }
            }),
            "visualContainers": [
                # Strategy Header
                {
                    "x": 20.0, "y": 15.0, "z": 1000.0, "width": 1240.0, "height": 55.0,
                    "config": json.dumps({
                        "name": "strategy_header",
                        "singleVisual": {
                            "visualType": "textbox",
                            "objects": {
                                "general": [{"properties": {"paragraphs": [
                                    {"textRuns": [{"value": "STRATEGIC OPERATIONAL ENGINE: 3-TIER ADAPTIVE DECISION MATRIX", "textStyle": {"fontWeight": "bold", "fontSize": "15pt", "color": "#F8FAFC"}}]},
                                    {"textRuns": [{"value": "Balancing user checkout friction with loss prevention: 98.45% of traffic receives frictionless auto-approval; high-risk triggers step-up verification.", "textStyle": {"fontSize": "9pt", "color": "#94A3B8"}}]}
                                ]}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Tier 1 Card
                {
                    "x": 20.0, "y": 80.0, "z": 2000.0, "width": 395.0, "height": 340.0,
                    "config": json.dumps({
                        "name": "tier1_card",
                        "singleVisual": {
                            "visualType": "textbox",
                            "objects": {
                                "general": [{"properties": {"paragraphs": [
                                    {"textRuns": [{"value": "TIER 1: FRICTIONLESS AUTO-APPROVE", "textStyle": {"fontWeight": "bold", "fontSize": "12pt", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n\n• Risk Score: < 0.30 (98.45% of Volume)", "textStyle": {"fontSize": "9.5pt", "color": "#E2E8F0"}}]},
                                    {"textRuns": [{"value": "\n• Action: Immediate Automated Authorization", "textStyle": {"fontSize": "9.5pt", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n• Customer Friction: ZERO (< 50ms latency)", "textStyle": {"fontSize": "9.5pt", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n• False Alarm Risk: Negligible (< 0.05%)", "textStyle": {"fontSize": "9.5pt", "color": "#E2E8F0"}}]},
                                    {"textRuns": [{"value": "\n• SLA: Real-Time Algorithmic Clearing", "textStyle": {"fontSize": "9.5pt", "color": "#94A3B8"}}]},
                                    {"textRuns": [{"value": "\n\nProtects checkout conversion rate and prevents customer cart abandonment.", "textStyle": {"fontSize": "8.5pt", "fontStyle": "italic", "color": "#94A3B8"}}]}
                                ]}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#10B981"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Tier 2 Card
                {
                    "x": 425.0, "y": 80.0, "z": 2001.0, "width": 395.0, "height": 340.0,
                    "config": json.dumps({
                        "name": "tier2_card",
                        "singleVisual": {
                            "visualType": "textbox",
                            "objects": {
                                "general": [{"properties": {"paragraphs": [
                                    {"textRuns": [{"value": "TIER 2: STEP-UP MFA CHALLENGE", "textStyle": {"fontWeight": "bold", "fontSize": "12pt", "color": "#F59E0B"}}]},
                                    {"textRuns": [{"value": "\n\n• Risk Score: 0.30 to 0.69 (1.25% of Volume)", "textStyle": {"fontSize": "9.5pt", "color": "#E2E8F0"}}]},
                                    {"textRuns": [{"value": "\n• Action: Trigger 3D-Secure 2.0 / OTP Push", "textStyle": {"fontSize": "9.5pt", "color": "#F59E0B"}}]},
                                    {"textRuns": [{"value": "\n• Customer Friction: 10s Self-Verification", "textStyle": {"fontSize": "9.5pt", "color": "#F59E0B"}}]},
                                    {"textRuns": [{"value": "\n• Fraud Prevention: Stops 99% of bots/phishing", "textStyle": {"fontSize": "9.5pt", "color": "#10B981"}}]},
                                    {"textRuns": [{"value": "\n• SLA: Dynamic In-Session Prompt", "textStyle": {"fontSize": "9.5pt", "color": "#94A3B8"}}]},
                                    {"textRuns": [{"value": "\n\nGracefully deflects account takeover without requiring manual staff intervention.", "textStyle": {"fontSize": "8.5pt", "fontStyle": "italic", "color": "#94A3B8"}}]}
                                ]}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#F59E0B"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Tier 3 Card
                {
                    "x": 830.0, "y": 80.0, "z": 2002.0, "width": 430.0, "height": 340.0,
                    "config": json.dumps({
                        "name": "tier3_card",
                        "singleVisual": {
                            "visualType": "textbox",
                            "objects": {
                                "general": [{"properties": {"paragraphs": [
                                    {"textRuns": [{"value": "TIER 3: AUTOMATED FREEZE & ALERT", "textStyle": {"fontWeight": "bold", "fontSize": "12pt", "color": "#EF4444"}}]},
                                    {"textRuns": [{"value": "\n\n• Risk Score: >= 0.70 (0.30% of Volume)", "textStyle": {"fontSize": "9.5pt", "color": "#E2E8F0"}}]},
                                    {"textRuns": [{"value": "\n• Action: Hard Decline + Card Temporary Lock", "textStyle": {"fontSize": "9.5pt", "color": "#EF4444"}}]},
                                    {"textRuns": [{"value": "\n• Notification: Instant SMS & Banking Push", "textStyle": {"fontSize": "9.5pt", "color": "#EF4444"}}]},
                                    {"textRuns": [{"value": "\n• Review Routing: Priority Fraud Desk Queue", "textStyle": {"fontSize": "9.5pt", "color": "#E2E8F0"}}]},
                                    {"textRuns": [{"value": "\n• SLA: < 5 Minutes Investigator Review", "textStyle": {"fontSize": "9.5pt", "color": "#94A3B8"}}]},
                                    {"textRuns": [{"value": "\n\nHalts unauthorized high-dollar fund extraction in real time.", "textStyle": {"fontSize": "8.5pt", "fontStyle": "italic", "color": "#94A3B8"}}]}
                                ]}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#EF4444"}}, "radius": 8}}]
                            }
                        }
                    })
                },
                # Strategic Policy Rules Table
                {
                    "x": 20.0, "y": 430.0, "z": 3000.0, "width": 1240.0, "height": 275.0,
                    "config": json.dumps({
                        "name": "policy_rules_table",
                        "singleVisual": {
                            "visualType": "tableEx",
                            "projections": {
                                "Values": [
                                    {"queryRef": "Dim_Risk_Tiers.Tier_Name"},
                                    {"queryRef": "Dim_Risk_Tiers.Risk_Min"},
                                    {"queryRef": "Dim_Risk_Tiers.Risk_Max"},
                                    {"queryRef": "Dim_Risk_Tiers.Policy_Action"},
                                    {"queryRef": "Dim_Risk_Tiers.Coverage_Volume_Pct"},
                                    {"queryRef": "Dim_Risk_Tiers.Customer_Friction"},
                                    {"queryRef": "Dim_Risk_Tiers.False_Alarm_Risk"},
                                    {"queryRef": "Dim_Risk_Tiers.SLA_Response"}
                                ]
                            },
                            "objects": {
                                "general": [{"properties": {"title": {"show": True, "text": "MULTI-TIER DECISION PROTOCOL SPECIFICATION & SERVICE LEVEL AGREEMENT (SLA)", "fontSize": 11, "fontColor": {"solid": {"color": "#F8FAFC"}}}}}],
                                "background": [{"properties": {"color": {"solid": {"color": "#1E293B"}}, "transparency": 0}}],
                                "border": [{"properties": {"show": True, "color": {"solid": {"color": "#334155"}}, "radius": 8}}]
                            }
                        }
                    })
                }
            ]
        }
    ]
}

with open(report_dir / "report.json", "w", encoding="utf-8") as f:
    json.dump(report_json, f, indent=2)

print("5. Packaging .pbit (Power BI Template)...")
# A .pbit is a ZIP file containing DataModelSchema, Report/Layout, [Content_Types].xml, Version, Settings, Metadata
pbit_path = pbi_dir / "Transactional_Fraud_Detection_Dashboard.pbit"

content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="application/xml" />
  <Override PartName="/Version" ContentType="application/vnd.ms-powerbi.version" />
  <Override PartName="/Settings" ContentType="application/vnd.ms-powerbi.settings" />
  <Override PartName="/Metadata" ContentType="application/vnd.ms-powerbi.metadata" />
  <Override PartName="/DataModelSchema" ContentType="application/vnd.ms-powerbi.datamodelschema" />
  <Override PartName="/Report/Layout" ContentType="application/vnd.ms-powerbi.reportlayout" />
</Types>"""

with zipfile.ZipFile(pbit_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types_xml)
    z.writestr("Version", "2.159.883.0".encode("utf-16le"))
    z.writestr("Settings", json.dumps({"version": 1}).encode("utf-16le"))
    z.writestr("Metadata", json.dumps({"version": 1}).encode("utf-16le"))
    z.writestr("DataModelSchema", json.dumps(model_bim, indent=2).encode("utf-8"))
    z.writestr("Report/Layout", json.dumps(report_json, indent=2).encode("utf-16le"))

print("Successfully generated all Power BI assets:")
print(f" - PBIP pointer: {pbi_dir / 'Transactional_Fraud_Detection_Dashboard.pbip'}")
print(f" - Semantic Model: {semantic_dir / 'model.bim'}")
print(f" - Report Layout: {report_dir / 'report.json'}")
print(f" - Power BI Template: {pbit_path}")


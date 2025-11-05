import pandas as pd
from sql import get_sec_ID


originations_filename = 'test_2'

report_date = '2001-01-01'
clientid = '44265'


originations = pd.read_excel(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\Loan_Orig_CPD\inputs\{originations_filename}.xlsx', header= 1)

## handle dates
originations['ExtendedMaturity_2'] = pd.to_datetime(originations['ExtendedMaturity_2'])
originations['ExtendedMaturity_2'] = originations['ExtendedMaturity_2'].dt.date

originations['ExtendedMaturity_1'] = pd.to_datetime(originations['ExtendedMaturity_1'])
originations['ExtendedMaturity_1'] = originations['ExtendedMaturity_1'].dt.date

originations['ExtendedMaturity_3'] = pd.to_datetime(originations['ExtendedMaturity_3'])
originations['ExtendedMaturity_3'] = originations['ExtendedMaturity_3'].dt.date

originations['ExtendedMaturity_4'] = pd.to_datetime(originations['ExtendedMaturity_4'])
originations['ExtendedMaturity_4'] = originations['ExtendedMaturity_4'].dt.date

originations['FinalMaturityDate'] = pd.to_datetime(originations['FinalMaturityDate'])
originations['FinalMaturityDate'] = originations['FinalMaturityDate'].dt.date

originations['RateCapMaturity'] = pd.to_datetime(originations['RateCapMaturity'])
originations['RateCapMaturity'] = originations['RateCapMaturity'].dt.date



# Create an empty list to hold the rows for Table 2
rows = []

# Iterate over each row in Table 1 to populate Table 2
for _, row in originations.iterrows():
    identifier = row['Identifier']
    # For each maturity type, map the value to Table 2
    for column in ['OriginalPrincipalAmount','Originator_1%','ExtendedMaturity_3','IndexRoundingInterval','CouponType','Closing Counsel','AuthorizedAmount','Originator_2%','IndexRounding','Originator_3%','Unfunded','ExtendedMaturity_2','RateCapMaturity','Loan Purpose','Originator_3','Originator_1','Originator_2','Intercompany','Sponsor','IndexFloor','CREFC Property Type','ExtendedMaturity_1','RateCapNotional','RateCapStrike','ExtendedMaturity_4','AmortizationType','Broker','IndexOffset','ReferenceIndex','Cross-Collateralized','FloaterSpread','FinalMaturityDate','HFS_HFI','CouponResetFrequency','City','State','PostalCode']:
        value = row[column]  # Get the value for this maturity type
        # Append the row with the identifier and value (if not None)
        if value is not None:
            rows.append({
                'Name': column,
                'ID': None,  # You can set IDs as needed
                'Value': value,
                'Identifier': identifier
            })

# Create the new Table 2 DataFrame
table2 = pd.DataFrame(rows)


mapping = {
    'ExtendedMaturity_1': 85493,
    'ExtendedMaturity_2': 85494,
    'ExtendedMaturity_3': 85495,
    'ExtendedMaturity_4': 85496,
    'FinalMaturityDate': 85497,
    'AuthorizedAmount': 85584,
    'OriginalPrincipalAmount': 85585,
    'Unfunded': 85586,
    'HFS_HFI': 85500,
    'Cross-Collateralized': 85597,
    'Intercompany': 84029,
    'CouponType': 85678,
    'ReferenceIndex': 85591,
    'CouponResetFrequency': 85593,
    'IndexOffset': 85520,
    'IndexRounding': 85502,
    'IndexRoundingInterval': 85503,
    'FloaterSpread': 85589,
    'IndexFloor': 85587,
    'RateCapNotional': 85504,
    'RateCapStrike': 85505,
    'RateCapMaturity': 85506,
    'AmortizationType': 85601,
    'CREFC Property Type': 85599,
    'Originator_1': 85509,
    'Originator_2': 85511,
    'Originator_3': 85513,
    'Originator_1%': 85510,
    'Originator_2%': 85512,
    'Originator_3%': 85514,
    'Closing Counsel': 85515,
    'Sponsor': 85516,
    'Broker': 85517,
    'Loan Purpose': 85518,
    'City': 85690,
    'State': 85692,
    'PostalCode': 85694
}

table2['ID'] = table2['Name'].map(mapping)

identifier_list = "', '".join(table2['Identifier'].tolist())
identifier_list = f"'{identifier_list}'"

## Get Security ID
security_ids = get_sec_ID(identifier_list)[0]
security_ids.rename(columns = {'Cusip': 'Identifier'}, inplace=True)



## Merge Security IDs 
merged_df = table2.merge(security_ids, on = 'Identifier', how = 'left')


merged_df.rename(columns= {'ID_x' : 'CPD ID', 'ID_y':'SecurityID'}, inplace=True)

print(merged_df.columns)

final_df = merged_df.copy()
final_df['ClientId'] = clientid
final_df['Reportdate'] = report_date
final_df['EndDate'] = ''


final_df = final_df[['Name','CPD ID','ClientId','SecurityID','Reportdate','EndDate', 'Value']]


final_df.to_excel(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\Loan_Orig_CPD\outputs\{originations_filename}.xlsx', index = False)

# Print the updated Table 2

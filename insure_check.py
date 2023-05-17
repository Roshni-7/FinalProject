import numpy as np
import streamlit as st
import joblib


#parameters for voting classifier model

months_as_customer=0                          
policy_deductable=0                         
umbrella_limit=0                                
capital_gains=0                                 
capital_loss=0                             
incident_hour_of_the_day=0                     
number_of_vehicles_involved=0                   
bodily_injuries=0                               
witnesses=0                                     
injury_claim=0                               
property_claim=0                             
vehicle_claim=0      
policy_csl_100_300=0                       
policy_csl_250_500=0                            
policy_csl_500_1000=0 
insured_sex_FEMALE=0                          
insured_sex_MALE=0      
insured_education_level_Associate=0                        
insured_education_level_College=0               
insured_education_level_High_School=0           
insured_education_level_JD=0                    
insured_education_level_MD=0                    
insured_education_level_Masters=0               
insured_education_level_PhD=0   
insured_occupation_adm_clerical=0                
insured_occupation_armed_forces=0               
insured_occupation_craft_repair=0               
insured_occupation_exec_managerial=0            
insured_occupation_farming_fishing=0            
insured_occupation_handlers_cleaners=0          
insured_occupation_machine_op_inspct=0          
insured_occupation_other_service=0              
insured_occupation_priv_house_serv=0            
insured_occupation_prof_specialty=0             
insured_occupation_protective_serv=0            
insured_occupation_sales=0                      
insured_occupation_tech_support=0               
insured_occupation_transport_moving=0 
insured_relationship_husband=0          
insured_relationship_not_in_family=0            
insured_relationship_other_relative=0           
insured_relationship_own_child=0                
insured_relationship_unmarried=0                
insured_relationship_wife=0   
incident_type_Multi_vehicle_Collision=0                  
incident_type_Parked_Car=0                      
incident_type_Single_Vehicle_Collision=0       
incident_type_Vehicle_Theft=0   
collision_type_Front_Collision=0                
collision_type_Rear_Collision=0                 
collision_type_Side_Collision=0 
incident_severity_Major_Damage=0                
incident_severity_Minor_Damage=0                
incident_severity_Total_Loss=0                  
incident_severity_Trivial_Damage=0 
authorities_contacted_Ambulance=0             
authorities_contacted_Fire=0                    
authorities_contacted_None=0                    
authorities_contacted_Other=0                   
authorities_contacted_Police=0    
property_damage_NO=0              
property_damage_YES=0  
police_report_available_NO=0                         
police_report_available_YES=0   

genuine_style = "<p style='font-size:24px; color:green;'>Insurance Claim is Genuine</p>"
fraud_style = "<p style='font-size:24px; color:red;'>Insurance Claim is Fraud</p>"


#Function for load and generate output from pretrained Voting Classifier model
def load_run_model():

    load_vc = joblib.load('model.pkl')
    load_scaler = joblib.load('scaler.pkl')

    data=[months_as_customer,policy_deductable,umbrella_limit,capital_gains,capital_loss,incident_hour_of_the_day,number_of_vehicles_involved,bodily_injuries,witnesses,injury_claim,property_claim,vehicle_claim,policy_csl_100_300,policy_csl_250_500,policy_csl_500_1000,insured_sex_FEMALE,insured_sex_MALE,insured_education_level_Associate,insured_education_level_College,insured_education_level_High_School,insured_education_level_JD,insured_education_level_MD,insured_education_level_Masters,insured_education_level_PhD,insured_occupation_adm_clerical,insured_occupation_armed_forces,insured_occupation_craft_repair,insured_occupation_exec_managerial,insured_occupation_farming_fishing,insured_occupation_handlers_cleaners,insured_occupation_machine_op_inspct,insured_occupation_other_service,insured_occupation_priv_house_serv,insured_occupation_prof_specialty,insured_occupation_protective_serv,insured_occupation_sales,insured_occupation_tech_support,insured_occupation_transport_moving,insured_relationship_husband,insured_relationship_not_in_family,insured_relationship_other_relative,insured_relationship_own_child,insured_relationship_unmarried,insured_relationship_wife,incident_type_Multi_vehicle_Collision,incident_type_Parked_Car,incident_type_Single_Vehicle_Collision,incident_type_Vehicle_Theft,collision_type_Front_Collision,collision_type_Rear_Collision,collision_type_Side_Collision,incident_severity_Major_Damage,incident_severity_Minor_Damage,incident_severity_Total_Loss,incident_severity_Trivial_Damage,authorities_contacted_Ambulance,authorities_contacted_Fire,authorities_contacted_None,authorities_contacted_Other,authorities_contacted_Police,property_damage_NO,property_damage_YES,police_report_available_NO,police_report_available_YES]

    data_need_scaler = data[:12]
    data_no_need_scaler = data[12:]
    data_scaled =  load_scaler.transform([data_need_scaler]) 
    data_non_scaled = np.reshape(data_no_need_scaler, (data_scaled.shape[0], -1))
    concatenated_test_data = np.concatenate((data_scaled, data_non_scaled), axis=1)

    pred = load_vc.predict(concatenated_test_data)
    return pred


#SToring resulit from function    
def display_result():
    result = load_run_model()
    if result == "N":
        st.markdown(genuine_style, unsafe_allow_html=True)
    if result == "Y":
        st.markdown(fraud_style, unsafe_allow_html=True)

def insure_check_application():   
    #The title
    
    st.title("InsureCheck - Insurance Fraud Claim Detection")

    #Content
    col1, col2, col3 = st.columns(3)

    #Personal Details
    with col1:
        st.subheader("Personal Details")
        #Insured Gender
        gender = st.radio("Insured Gender",('MALE','FEMALE'))
        if gender == 'MALE':
            insured_sex_MALE=1
            insured_sex_FEMALE=0
        else:
            insured_sex_MALE=0  
            insured_sex_FEMALE=1

        #Insured Education Qualification
        education = st.selectbox("Insured Education Qualification",('Associate','High School','College','JD (Juris Doctor/Law Degree)','MD (Doctor of Medicine)','Masters','PhD'))
        if education == 'High School':
            insured_education_level_Associate=0
            insured_education_level_College=0               
            insured_education_level_High_School=1           
            insured_education_level_JD=0                    
            insured_education_level_MD=0                    
            insured_education_level_Masters=0               
            insured_education_level_PhD=0  
        if education == 'College':
            insured_education_level_Associate=0
            insured_education_level_College=1               
            insured_education_level_High_School=0           
            insured_education_level_JD=0                    
            insured_education_level_MD=0                    
            insured_education_level_Masters=0               
            insured_education_level_PhD=0  
        if education == 'JD (Juris Doctor/Law Degree)':
            insured_education_level_Associate=0
            insured_education_level_College=0               
            insured_education_level_High_School=0           
            insured_education_level_JD=1                    
            insured_education_level_MD=0                    
            insured_education_level_Masters=0               
            insured_education_level_PhD=0 
        if education == 'MD (Doctor of Medicine)':
            insured_education_level_Associate=0
            insured_education_level_College=0               
            insured_education_level_High_School=0           
            insured_education_level_JD=0                    
            insured_education_level_MD=1                    
            insured_education_level_Masters=0               
            insured_education_level_PhD=0 
        if education == 'Masters':
            insured_education_level_Associate=0
            insured_education_level_College=0               
            insured_education_level_High_School=0           
            insured_education_level_JD=0                    
            insured_education_level_MD=0                    
            insured_education_level_Masters=1               
            insured_education_level_PhD=0 
        if education == 'PhD':
            insured_education_level_Associate=0
            insured_education_level_College=0               
            insured_education_level_High_School=0           
            insured_education_level_JD=0                    
            insured_education_level_MD=0                    
            insured_education_level_Masters=0               
            insured_education_level_PhD=1 
        if education == 'Associate':
            insured_education_level_Associate=1
            insured_education_level_College=0               
            insured_education_level_High_School=0           
            insured_education_level_JD=0                    
            insured_education_level_MD=0                    
            insured_education_level_Masters=0               
            insured_education_level_PhD=0 


        #Insured Occupation
        occupation = st.selectbox("Insured Occupation",('Administrative Clerk','Craftsmen/Repair','Machine Operator Inspector','Sales','Armed forces','Techical support',
        'Professional Job','Private house servents','Executive managerial',
        'Protective servents','Transportion service','Handlers/Cleaners',
        'Farming/Fishing','Others'))
        if occupation == 'Administrative Clerk':
            insured_occupation_adm_clerical=1
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0  
        if occupation == 'Craftsmen/Repair':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=1               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0  
        if occupation == 'Machine Operator Inspector':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=1          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0
        if occupation == 'Sales':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=1                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0
        if occupation == 'Armed forces':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=1               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0
        if occupation == 'Techical support':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=1               
            insured_occupation_transport_moving=0      
        if occupation == 'Professional Job':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=1             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0   
        if occupation == 'Private house servents':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=1            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0      
        if occupation == 'Executive managerial':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=1            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0   
        if occupation == 'Protective servents':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=1            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0   
        if occupation == 'Transportion service':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=1   
        if occupation == 'Handlers/Cleaners':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=1          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0  
        if occupation == 'Farming/Fishing':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=1            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=0              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0 
        if occupation == 'Others':
            insured_occupation_adm_clerical=0
            insured_occupation_armed_forces=0               
            insured_occupation_craft_repair=0               
            insured_occupation_exec_managerial=0            
            insured_occupation_farming_fishing=0            
            insured_occupation_handlers_cleaners=0          
            insured_occupation_machine_op_inspct=0          
            insured_occupation_other_service=1              
            insured_occupation_priv_house_serv=0            
            insured_occupation_prof_specialty=0             
            insured_occupation_protective_serv=0            
            insured_occupation_sales=0                      
            insured_occupation_tech_support=0               
            insured_occupation_transport_moving=0 
    
    

        #Insured Relationship
        relationship = st.selectbox("Insured Relationship",('Husband','Other relative','Own child','Unmarried','Wife','Not in family'))
        if relationship == 'Other relative':
            insured_relationship_husband=0
            insured_relationship_not_in_family=0            
            insured_relationship_other_relative=1           
            insured_relationship_own_child=0                
            insured_relationship_unmarried=0                
            insured_relationship_wife=0
        if relationship == 'Own child':
            insured_relationship_husband=0
            insured_relationship_not_in_family=0            
            insured_relationship_other_relative=0           
            insured_relationship_own_child=1                
            insured_relationship_unmarried=0                
            insured_relationship_wife=0
        if relationship == 'Unmarried':
            insured_relationship_husband=0
            insured_relationship_not_in_family=0            
            insured_relationship_other_relative=0           
            insured_relationship_own_child=0                
            insured_relationship_unmarried=1                
            insured_relationship_wife=0
        if relationship == 'Wife':
            insured_relationship_husband=0
            insured_relationship_not_in_family=0            
            insured_relationship_other_relative=0           
            insured_relationship_own_child=0                
            insured_relationship_unmarried=0                
            insured_relationship_wife=1  
        if relationship == 'Not in family':
            insured_relationship_husband=0
            insured_relationship_not_in_family=1            
            insured_relationship_other_relative=0           
            insured_relationship_own_child=0                
            insured_relationship_unmarried=0                
            insured_relationship_wife=0  
        if relationship == 'Husband':
            insured_relationship_husband=1
            insured_relationship_not_in_family=0            
            insured_relationship_other_relative=0           
            insured_relationship_own_child=0                
            insured_relationship_unmarried=0                
            insured_relationship_wife=0  

    #Insurance Details
    with col2:
        st.subheader("Insurance Details")
        #Policy CSL (Combined Single Limits)
        csl = st.selectbox("Policy CSL (Combined Single Limits)",('100/300','250/500','500/1000'))
        if csl == '250/500':
            policy_csl_100_300=0
            policy_csl_250_500=1                            
            policy_csl_500_1000=0 
        if csl == '500/1000':
            policy_csl_100_300=0
            policy_csl_250_500=0                            
            policy_csl_500_1000=1 
        if csl == '100/300':
            policy_csl_100_300=1
            policy_csl_250_500=0                            
            policy_csl_500_1000=0    

        #months as customer
        months = st.number_input('Months as customer',value=0, step=1, format='%d')
        months_as_customer=months

        #policy deductable
        deductable = st.number_input('Policy deductable for customer',value=0, step=1, format='%d')
        policy_deductable=deductable  

        #Umberlla Limit
        u_limit = st.number_input('Umbrella Limit for customer',value=0, step=1, format='%d')
        umbrella_limit=u_limit

        #Capital Gains
        gain = st.number_input('Capital Gain of customer',value=0, step=1, format='%d')
        capital_gains=gain

        #Capital Loss
        loss = st.number_input('Capital Loss of customer',value=0, step=1, format='%d')
        capital_loss=0-loss


    #Insurance Claim Details
    with col3:
        st.subheader("Insurance Claim Details")
        #Incident Hrs of the day
        ihrsd = st.number_input('Incident Hrs of the day',value=0, step=1, format='%d')
        incident_hour_of_the_day=ihrsd

        #Number of vehicles involved
        vehicles = st.number_input('Number of vehicles involved',value=0, step=1, format='%d')
        number_of_vehicles_involved=vehicles

        #bodily injuries
        bi = st.number_input('Bodily Injuries',value=0, step=1, format='%d')
        bodily_injuries=bi

        #Witnesses
        w = st.number_input('Number of Witnesses',value=0, step=1, format='%d')
        witnesses=w
        
        #Injury Claim
        injury= st.number_input('Injury Claim',value=0, step=1, format='%d')
        injury_claim=injury

        #Property Claim
        property = st.number_input('Property Claim',value=0, step=1, format='%d')
        property_claim=property 

        #vehicle Claim
        vehicle = st.number_input('Vehicle Claim',value=0, step=1, format='%d')
        vehicle_claim=vehicle
        

        #Inccident Type
        itype = st.selectbox("Inccident Type",('Multi Vehicle Collision','Single Vehicle Collision','Vehicle Theft','Parked Car'))
        if itype == 'Single Vehicle Collision':
            incident_type_Multi_vehicle_Collision=0
            incident_type_Parked_Car=0                      
            incident_type_Single_Vehicle_Collision=1       
            incident_type_Vehicle_Theft=0 
        if itype == 'Vehicle Theft':
            incident_type_Multi_vehicle_Collision=0
            incident_type_Parked_Car=0                      
            incident_type_Single_Vehicle_Collision=0       
            incident_type_Vehicle_Theft=1
        if itype == 'Parked Car':
            incident_type_Multi_vehicle_Collision=0
            incident_type_Parked_Car=1                      
            incident_type_Single_Vehicle_Collision=0       
            incident_type_Vehicle_Theft=0 
        if itype == 'Multi Vehicle Collision':
            incident_type_Multi_vehicle_Collision=1
            incident_type_Parked_Car=0                      
            incident_type_Single_Vehicle_Collision=0       
            incident_type_Vehicle_Theft=0 

        #Collision Type
        ctype = st.selectbox("Collision Type",('Front Collision','Side Collision','Rear Collision'))
        if ctype == 'Side Collision':
            collision_type_Front_Collision=0
            collision_type_Rear_Collision=0                 
            collision_type_Side_Collision=1
        if ctype == 'Rear Collision':
            collision_type_Front_Collision=0
            collision_type_Rear_Collision=0                 
            collision_type_Side_Collision=1
        if ctype == 'Front Collision':
            collision_type_Front_Collision=1
            collision_type_Rear_Collision=0                 
            collision_type_Side_Collision=0

        #incident severity
        severity = st.selectbox("Incident Severity",('Major Damage','Minor Damage','Total Loss','Trivial Damage'))
        if severity == 'Minor Damage':
            incident_severity_Major_Damage=0
            incident_severity_Minor_Damage=1                
            incident_severity_Total_Loss=0                  
            incident_severity_Trivial_Damage=0 
        if severity == 'Total Loss':
            incident_severity_Major_Damage=0
            incident_severity_Minor_Damage=0                
            incident_severity_Total_Loss=1                  
            incident_severity_Trivial_Damage=0   
        if severity == 'Trivial Damage':
            incident_severity_Major_Damage=0
            incident_severity_Minor_Damage=0                
            incident_severity_Total_Loss=0                  
            incident_severity_Trivial_Damage=1    
        if severity == 'Major Damage':
            incident_severity_Major_Damage=1
            incident_severity_Minor_Damage=0                
            incident_severity_Total_Loss=0                  
            incident_severity_Trivial_Damage=0  


        #authorities contacted
        authorities = st.selectbox("Authorities Contacted",('Ambulance','Police','Fire','Other','None'))
        if authorities == 'Police':
            authorities_contacted_Ambulance=0
            authorities_contacted_Fire=0                    
            authorities_contacted_None=0                   
            authorities_contacted_Other=0                   
            authorities_contacted_Police=1  
        if authorities == 'Fire':
            authorities_contacted_Ambulance=0
            authorities_contacted_Fire=1                    
            authorities_contacted_None=0                   
            authorities_contacted_Other=0                   
            authorities_contacted_Police=0  
        if authorities == 'Other':
            authorities_contacted_Ambulance=0
            authorities_contacted_Fire=0                    
            authorities_contacted_None=0                   
            authorities_contacted_Other=1                   
            authorities_contacted_Police=0 
        if authorities == 'None':
            authorities_contacted_Ambulance=0
            authorities_contacted_Fire=0                    
            authorities_contacted_None=1                   
            authorities_contacted_Other=0                   
            authorities_contacted_Police=0  
        if authorities == 'Ambulance':
            authorities_contacted_Ambulance=1
            authorities_contacted_Fire=0                    
            authorities_contacted_None=0                   
            authorities_contacted_Other=0                   
            authorities_contacted_Police=0  

        #Property Damage
        pd = st.checkbox("Property Damage ?")
        if pd:
            property_damage_YES=1
            property_damage_NO=0
        else:
            property_damage_YES=0
            property_damage_NO=1
        

        #Police Report Available
        pr = st.checkbox("Police Report Available ?")
        if pr:
            police_report_available_YES=1
            police_report_available_NO=0
        else:
            police_report_available_YES=0
            police_report_available_NO=1

    #Submit Button
    if st.button(label="CHECK"):
        display_result()


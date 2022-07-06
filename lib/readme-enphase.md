
# Web Access

Default username and password are `envoy` and last six digits of the serial number.  
See [article](https://support.enphase.com/s/article/What-is-the-Username-and-Password-for-the-Administration-page-of-the-Envoy-local-interface)

user: `envoy`
password: `132576`


# API Access

Account [details](https://enlighten.enphaseenergy.com/account) page show my user ID.   

# Python module 

Ken Clifton has a [python module](https://github.com/ken-clifton/Enphase-Envoy-S-Inventory-Python)
to inventory the system.  He also has a blog with [walkthrough of the module](https://www.kenclifton.com/wordpress/2017/06/enphase-envoy-s-per-panel-python-script-walkthrough/)


# envoy.local

Support [discussion](https://stackoverflow.com/questions/352098/how-can-i-pretty-print-json-in-a-shell-script)

Notes on [URLs](http://guytec.com/Envoy-S/)

The system can be accessed at envoy.local.  Some settings require username and password.  

http://envoy.local/ivp/meters/readings


## http://envoy.local/production.json 

	curl http://envoy.local/production.json  | python -m json.tool > production.json





	/admin/lib/acb_config.json
	/admin/lib/admin_dcc_display.json
	/admin/lib/admin_pmu_display.json
	/admin/lib/date_time_display.json
	/admin/lib/date_time_display.json?tzlist=1
	/admin/lib/date_time_display.json?tzlist=1&locale=en
	/admin/lib/dba.json
	/admin/lib/network_display.json
	/admin/lib/network_display.json?cellular=1
	/admin/lib/security_display.json
	/admin/lib/tariff.json
	/admin/lib/wireless_display.json
	/admin/lib/wireless_display.json?site_info=0
	/api/v1/production/inverters
	/datatab/event_dt.rb
	/datatab/event_dt.rb?start=0&length=153
	/home.json
	/info.xml
	/installer/agf/details.json
	/installer/agf/index.json?simplified=true
	/installer/agf/inverters_status.json
	/installer/agf/set_profile.json
	/installer/pcu_comm_check
	/installer/profiles/details.json
	/installer/profiles/index.json
	/installer/profiles/inverters_status.json
	/installer/profiles/set_profile.json
	/inventory.json
	/inventory.json?deleted=1
	/ivp/grest/local/gs/redeterminephase
	/ivp/meters
	/ivp/meters/cts
	/ivp/meters/cts/EID
	/ivp/meters/EID
	/ivp/meters/readings
	/ivp/mod/EID/mode/power
	/ivp/peb/newscan
	/ivp/peb/reportsettings
	/ivp/tpm/capability
	/ivp/tpm/parameters
	/ivp/tpm/select
	/ivp/tpm/tpmstatus
	/production.json
	/production.json?details=1
	/prov
	/stream/meter
	/stream/psd


# /ivp/meters:

	[
		{
			"eid": 704643328,
			"state": "enabled",
			"measurementType": "production",
			"phaseMode": "split",
			"phaseCount": 2,
			"meteringStatus": "normal",
			"statusFlags": []
		},
		{
			"eid": 704643584,
			"state": "enabled",
			"measurementType": "net-consumption",
			"phaseMode": "split",
			"phaseCount": 2,
			"meteringStatus": "normal",
			"statusFlags": []
		}
	]

# /vp/meters/EID 

Get specific meter

# /ivp/meters/cts

Forbidden

# /ivp/meters/readings

	[
		{
			"eid": 704643328,
			"timestamp": 1655613082,
			"actEnergyDlvd": 1545246.269,
			"actEnergyRcvd": 0.002,
			"apparentEnergy": 1863274.016,
			"reactEnergyLagg": 563086.856,
			"reactEnergyLead": 0.000,
			"instantaneousDemand": 0.000,
			"activePower": 0.000,
			"apparentPower": 520.492,
			"reactivePower": 511.486,
			"pwrFactor": 0.000,
			"voltage": 244.626,
			"current": 4.255,
			"freq": 60.000,
			"channels": [
				{
					"eid": 1778385169,
					"timestamp": 1655613082,
					"actEnergyDlvd": 771484.129,
					"actEnergyRcvd": 0.000,
					"apparentEnergy": 930785.885,
					"reactEnergyLagg": 284040.078,
					"reactEnergyLead": 0.000,
					"instantaneousDemand": -0.000,
					"activePower": -0.000,
					"apparentPower": 260.126,
					"reactivePower": 255.957,
					"pwrFactor": 0.000,
					"voltage": 122.392,
					"current": 2.126,
					"freq": 60.000
				},
				{
					"eid": 1778385170,
					"timestamp": 1655613082,
					"actEnergyDlvd": 773762.140,
					"actEnergyRcvd": 0.002,
					"apparentEnergy": 932488.130,
					"reactEnergyLagg": 279046.778,
					"reactEnergyLead": 0.000,
					"instantaneousDemand": 0.000,
					"activePower": 0.000,
					"apparentPower": 260.367,
					"reactivePower": 255.528,
					"pwrFactor": 0.000,
					"voltage": 122.234,
					"current": 2.129,
					"freq": 60.000
				},
				{
					"eid": 1778385171,
					"timestamp": 1655613082,
					"actEnergyDlvd": 0.000,
					"actEnergyRcvd": 0.000,
					"apparentEnergy": 0.000,
					"reactEnergyLagg": 0.000,
					"reactEnergyLead": 0.000,
					"instantaneousDemand": 0.000,
					"activePower": 0.000,
					"apparentPower": 0.000,
					"reactivePower": 0.000,
					"pwrFactor": 0.000,
					"voltage": 0.000,
					"current": 0.000,
					"freq": 60.000
				}
			]
		},
		{
			"eid": 704643584,
			"timestamp": 1655613082,
			"actEnergyDlvd": 553369.752,
			"actEnergyRcvd": 1025652.268,
			"apparentEnergy": 2362072.293,
			"reactEnergyLagg": 1654.034,
			"reactEnergyLead": 1345350.733,
			"instantaneousDemand": 529.666,
			"activePower": 529.666,
			"apparentPower": 1440.389,
			"reactivePower": -1234.542,
			"pwrFactor": 0.375,
			"voltage": 244.705,
			"current": 11.768,
			"freq": 60.000,
			"channels": [
				{
					"eid": 1778385425,
					"timestamp": 1655613082,
					"actEnergyDlvd": 231617.382,
					"actEnergyRcvd": 527208.971,
					"apparentEnergy": 1182713.072,
					"reactEnergyLagg": 1547.063,
					"reactEnergyLead": 695051.110,
					"instantaneousDemand": 129.359,
					"activePower": 129.359,
					"apparentPower": 700.010,
					"reactivePower": -651.771,
					"pwrFactor": 0.196,
					"voltage": 122.451,
					"current": 5.715,
					"freq": 60.000
				},
				{
					"eid": 1778385426,
					"timestamp": 1655613082,
					"actEnergyDlvd": 321752.370,
					"actEnergyRcvd": 498443.296,
					"apparentEnergy": 1179359.221,
					"reactEnergyLagg": 106.971,
					"reactEnergyLead": 650299.623,
					"instantaneousDemand": 400.307,
					"activePower": 400.307,
					"apparentPower": 740.379,
					"reactivePower": -582.772,
					"pwrFactor": 0.545,
					"voltage": 122.255,
					"current": 6.053,
					"freq": 60.000
				},
				{
					"eid": 1778385427,
					"timestamp": 1655613082,
					"actEnergyDlvd": 0.000,
					"actEnergyRcvd": 0.000,
					"apparentEnergy": 0.000,
					"reactEnergyLagg": 0.000,
					"reactEnergyLead": 0.000,
					"instantaneousDemand": 0.000,
					"activePower": 0.000,
					"apparentPower": 0.000,
					"reactivePower": 0.000,
					"pwrFactor": 0.000,
					"voltage": 0.000,
					"current": 0.000,
					"freq": 60.000
				}
			]
		}
	]


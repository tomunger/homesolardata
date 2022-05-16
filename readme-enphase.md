
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
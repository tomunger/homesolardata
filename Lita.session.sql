use enphasebackup;


select * from enphasetest.production 
order by datetime desc limit 100;

-- delete from enphasesolar.gather 

select datetime, consumption, production from enphasetest.production where datetime > '2022-05-24'


insert into enphasesolar.gather (datetime, consumption, production) 
		(select datetime, consumption, production 
				from enphasetest.production 
				where datetime > '2022-05-24'
				order by datetime)

--
-- Get the records around the gap
select * from enphasetest.production where production_key >= 267521 and production_key <= 267522


--
-- Get the records between the gap
insert into enphasetest.production (datetime, consumption, production) 
		(select datetime, consumption, production 
				from enphasesolar.production 
				where datetime > '2022-05-22 18:03:28.84' and datetime < '2022-05-22 19:22:34.42'
				order by datetime)


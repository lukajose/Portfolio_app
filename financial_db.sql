
drop table if exists Asset cascade;
drop table if exists hasDaily;
drop table if exists DailyData;

create table Asset(
    id integer,
    ticker text,
    asset_type text,
    isTrading boolean,
    primary key (id)
);

create table hasDaily(
    asset_id integer,
    reg_date double PRECISION, --- epoch time
    update_date double PRECISION, -- epoch time
    foreign key (asset_id) references Asset(id)
);

create table DailyData(
    day date,
    asset_id integer,
    high numeric,
    low numeric, 
    open numeric,
    close numeric,
    volume numeric,
    adj_close numeric,
    foreign key (asset_id) references Asset(id)
);
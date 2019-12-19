
--drop table if exists Asset cascade;
--drop table if exists hasDaily;
--drop table if exists DailyData;

create table if not exists Equities(
    id integer,
    ticker text,
    asset_type text,
    isTrading boolean,
    primary key (id)
);

create table if not exists hasDaily(
    asset_id integer,
    reg_date double PRECISION, --- epoch time
    update_date double PRECISION, -- epoch time
    foreign key (asset_id) references Equities(id)
);

create table if not exists DailyData_Equities(
    day date,
    asset_id integer,
    high numeric,
    low numeric, 
    open numeric,
    close numeric,
    volume numeric,
    adj_close numeric,
    foreign key (asset_id) references Equities(id)
);

create table if not exists Market(
    id integer,
    ticker text,
    name_market text,
    country text,
    primary key (id)
);

create table if not exists DailyData_Market(
    day date,
    market_id integer,
    high numeric,
    low numeric, 
    open numeric,
    close numeric,
    volume numeric,
    adj_close numeric,
    foreign key (market_id) references Market(id)
);

create table if not exists CAPM(
    asset_id integer,
    market_id integer,
    alpha numeric,
    Beta numeric,
    R_sq numeric,
    foreign key (asset_id) references Equities(id),
    foreign key (market_id) references Market(id)
);

create table if not exists RiskFree(
    id integer,
    ticker text,
    desc_rf text,
    country text,
    primary key (id)
);

create table if not exists DailyData_RiskFree(
    day date,
    riskfree_id integer,
    high numeric,
    low numeric, 
    open numeric,
    close numeric,
    volume numeric,
    adj_close numeric,
    foreign key (riskfree_id) references RiskFree(id)
);

create table if not exists EquitiesStats(
    asset_id integer,
    avg_return numeric,
    variance numeric,
    foreign key (asset_id) references Equities(id)
);
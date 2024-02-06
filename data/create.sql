CREATE TABLE IF NOT EXISTS calendar (
    date VARCHAR(255) NOT NULL,
    wm_yr_wk INTEGER NOT NULL,
    weekday VARCHAR(255) NOT NULL,
    wday INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    event_name_1 VARCHAR(255),
    event_type_1 VARCHAR(255),
    event_name_2 VARCHAR(255),
    event_type_2 VARCHAR(255),         
    snap_ca INTEGER NOT NULL,
    snap_tx INTEGER NOT NULL,
    snap_wi INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (date)
);


CREATE TABLE IF NOT EXISTS prices (
    key VARCHAR(255) NOT NULL,
    store_id VARCHAR(255) NOT NULL,
    item_id VARCHAR(255) NOT NULL,
    wm_yr_wk INTEGER NOT NULL,
    sell_price FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (key)
);


CREATE TABLE IF NOT EXISTS sales (
    key VARCHAR(255) NOT NULL,
    id VARCHAR(255) NOT NULL,    
    item_id VARCHAR(255) NOT NULL,
    dept_id VARCHAR(255) NOT NULL,
    cat_id VARCHAR(255) NOT NULL,
    store_id VARCHAR(255) NOT NULL,
    state_id VARCHAR(255) NOT NULL,
    date_id INTEGER NOT NULL,
    sales FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (key)
);

CREATE TABLE IF NOT EXISTS prediction (
    store_id VARCHAR(255) NOT NULL,
    item_id VARCHAR(255) NOT NULL,
    date_id INTEGER NOT NULL,
    prediction FLOAT NOT NULL,
    mlflow_experiment_id  INTEGER NOT NULL,
    mlflow_run_id  VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (store_id, item_id, date_id)
);

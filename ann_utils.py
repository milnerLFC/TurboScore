import pandas as pd
from sklearn.preprocessing import StandardScaler


def split_data(data,fixtures,test_size,game_infos,over_cols,odds,target, no_red = True):
    if no_red:
        print(len(data))
        data = data[(data['HR'] == 0.) & (data['AR'] == 0.)].copy().reset_index()
        print(len(data))

    train_data = data.iloc[:-(test_size+len(fixtures))]
    test_data = data.iloc[-(test_size+len(fixtures)):-len(fixtures)]
    predict_data = data.iloc[-len(fixtures):]
    
    train_data = train_data.dropna(subset=[target])
    nan_rows_in_test = test_data[test_data[target].isna()]
    predict_data = pd.concat([predict_data, nan_rows_in_test])
    test_data = test_data.dropna(subset=[target])
    
    predict_data = predict_data.sort_values(by='DateTime')
    
    X_train = train_data.drop(game_infos+over_cols+odds+['R'], axis=1)
    y_train = train_data[target]
    meta_train = train_data[game_infos+odds]

    X_test = test_data.drop(game_infos+over_cols+odds+['R'], axis=1)
    y_test = test_data[target]
    meta_test = test_data[game_infos+odds]


    X_pred = predict_data.drop(game_infos+over_cols+odds+['R'], axis=1)
    meta_pred = predict_data[game_infos+odds]

    return X_train,y_train,meta_train,X_test,y_test,meta_test,X_pred,meta_pred

def scale_datasets(X_train,X_test,X_pred):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    X_pred_scaled = scaler.transform(pd.concat([X_test,X_pred]))
    
    return X_train_scaled,X_test_scaled,X_pred_scaled

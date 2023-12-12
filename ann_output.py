import pandas as pd

def binary_ann_df(model,X_test_scaled,meta_test):
    all_predictions_ann = model.predict(X_test_scaled)
    prob = all_predictions_ann[:, 0]

    result_df_ann = pd.DataFrame({
        'yes': prob,
        'no': 1-prob,
    })

    result_df_ann = pd.concat([meta_test.reset_index(drop=True), result_df_ann], axis=1)
    result_df_ann.tail(20)
    
    return result_df_ann
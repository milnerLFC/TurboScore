from sklearn.neural_network import MLPClassifier

def mlp_model_fit(X_train_scaled,y_train):
    
    mlp_model = MLPClassifier(hidden_layer_sizes=(2**2, 2**3), 
                                activation='relu', 
                                max_iter=800, 
                                learning_rate_init = 0.005,
                                # power_t=0.5, 
                                # validation_fraction=0.1, 
                                # beta_1=0.9, beta_2=0.999,
                                # epsilon=1e-08,
                                random_state=42)
    
    return mlp_model.fit(X_train_scaled, y_train)
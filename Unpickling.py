import pickle

try:
    with open('scaler.pkl', 'rb') as f:
        data = pickle.load(f)
    print("Unpickling successful.")
except Exception as e:
    print(f"Error during unpickling: {e}")
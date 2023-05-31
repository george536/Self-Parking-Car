from data_collection.parking_labeller import parking_labeller


if __name__ == '__main__':
    labeller = parking_labeller(load_world='Town05')
    labeller.run()
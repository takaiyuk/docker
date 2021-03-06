import lightgbm as lgb


def test_fit_gpu():
    X = [[0,1,2],[3,4,5]]
    y = [0,1]
    m = lgb.LGBMClassifier(device="gpu", gpu_platform_id=0, gpu_device_id=0)
    m.fit(X,y)
    print(m.predict(X))

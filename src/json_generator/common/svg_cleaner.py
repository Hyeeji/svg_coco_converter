# 문자열 필터링 함수
def correct_id(w):
        w = w.replace("_x5F", "").replace("_x3", "").replace("__x2A_", "~").replace("_x2A_", "~").replace("__", "_")
        try:
            if w[-1:] == "_":
                temp_w = ''
                if w[-3:-2] == "_":
                    temp_w_sp = w.split("_")
                    temp_w = '_'.join(temp_w_sp[:-2])
                elif w[-4:-3] == "_":
                    temp_w_sp = w.split("_")
                    if len(temp_w_sp) > 3:
                        temp_w = '_'.join(temp_w_sp[:-3])
                    else:
                        temp_w = '_'.join(temp_w_sp[:-2])
                if len(temp_w) > 0:
                    w = temp_w
        except:
            pass
        if w[-1:] == "_":
            w = w[:-1]
        return w.lower()

# 입력 값인 w는 각 엘리먼트의 id를 뜻함.
# 위 함수를 거쳐 나온 문자열이 원본 문자열.
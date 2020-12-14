
from flask import Flask, render_template, request
from werkzeug.utils import redirect
import datetime

app = Flask(__name__)

# 全域變數
serial_num = 0
custom_code = 0
mode_code = 0
acc = 0
cause = 0

@app.route('/', methods=['POST','GET'])
def hello():
    # 當 Server 端接到 POST (按鈕)的消息，接收該網頁表單的資訊
    print(request.method)
    if request.method == 'POST':
        print('>> {}'.format(request.values['serial_num'])) 

        datetime_dt = datetime.datetime.today()# 當地時間
        datetime_str = datetime_dt.strftime('%Y%m%d%H%M%S')  # 格式化日期
        date_str = datetime_dt.strftime('%Y%m%d')

        with open('record_{}.log'.format(date_str), 'a+') as log_file:
            log_file.write('{}, 開始維修, \n'.format(datetime_str))

        return redirect('/second', code=307)

    # 當 Server 端接收到的是普通的 GET 時，導到 main.html 頁面            
    return  render_template('main.html')
    

@app.route('/second', methods=['POST', 'GET'])
def second():
    global serial_num, cause
    try:
        if request.values['ooo'] != "":
            print('>>> {}'.format(request.values['ooo']))
            cause = request.values['ooo']

            # return render_template('third.html', cause=cause)
            return redirect('/third', code=307)

    except:
        print('At Second Page')
        print('Got:')
        print('{}'.format(request.values['serial_num']))
        serial_num = request.values['serial_num']

        return render_template('second.html', serial_num=serial_num)


@app.route('/third', methods=['POST', 'GET'])
def third():
    global serial_num, cause

    try:
        cause = request.values['ooo']
        print('>> ' + \
            str(serial_num) + \
            " : " + \
            str(cause))
        
        out = str(serial_num) + \
            " : " + \
            str(cause)

        return render_template('third.html', cause=cause, serial_num=serial_num)

    except:
        fault_type = request.values['fault_type']

        print('> {}'.format(serial_num))
        print('> {}'.format(custom_code))
        print('> {}'.format(mode_code))
        print('> {}'.format(acc))
        print('> {}'.format(cause))
        print('> {}'.format(fault_type))

        datetime_dt = datetime.datetime.today()# 當地時間
        datetime_str = datetime_dt.strftime('%Y%m%d%H%M%S')  # 格式化日期
        date_str = datetime_dt.strftime('%Y%m%d')

        with open('record_{}.log'.format(date_str), 'a+') as log_file:
            log_file.write('{}, {}, {}\n'.format(
                datetime_str,
                cause,
                fault_type))
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

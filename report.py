#!/usr/bin/python3
import requests
import random
import time
import re
import execjs
import sys


def login(sess, uname, pwd):
    salt_url = 'http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/index.do'
    salt_response = sess.get(salt_url)
    salt_response.encoding = 'utf-8'
    lt = re.search('name="lt" value="(.*?)"', salt_response.text).group(1)
    salt = re.search('id="pwdDefaultEncryptSalt" value="(.*?)"', salt_response.text).group(1)
    execution = re.search('name="execution" value="(.*?)"', salt_response.text).group(1)
    f = open("encrypt.js", 'r', encoding='UTF-8')
    line = f.readline()
    js = ''
    while line:
        js = js + line
        line = f.readline()
    ctx = execjs.compile(js)
    password = ctx.call('_ep', pwd, salt)

    login_url = 'https://newids.seu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.seu.edu.cn%2Fqljfwapp2%2Fsys%2FlwReportEpidemicSeu%2Findex.do'
    personal_info = {'username': uname,
                     'password': password,
                     'lt': lt,
                     'dllt': 'userNamePasswordLogin',
                     'execution': execution,
                     '_eventId': 'submit',
                     'rmShown': '1'}
    login_response = sess.post(login_url, personal_info)
    login_response.encoding = 'utf-8'

    if re.search("学院", login_response.text):
        print("登陆成功!")
    else:
        print("登陆失败!请检查一卡通号和密码。")
        raise


def get_header(sess, cookie_url):
    cookie_response = sess.get(cookie_url)
    weu = requests.utils.dict_from_cookiejar(cookie_response.cookies)['_WEU']
    cookie = requests.utils.dict_from_cookiejar(sess.cookies)

    header = {'Referer': 'http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/index.do',
              'Cookie': '_WEU=' + weu + '; MOD_AUTH_CAS=' + cookie['MOD_AUTH_CAS'] + ';'}
    return header


def get_info(sess, header):
    info_url = 'http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/modules/dailyReport/getMyDailyReportDatas.do'
    info_response = sess.post(info_url, data={'rysflb': 'BKS', 'pageSize': '10', 'pageNumber': '1'}, headers=header)
    return info_response


def report(sess):
    try:
        cookie_url = 'http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/configSet/noraml/getRouteConfig.do'
        header = get_header(sess, cookie_url)
        info = get_info(sess, header)
        if info.status_code == 403:
            raise
    except:
        cookie_url2 = 'http://ehall.seu.edu.cn/qljfwapp2/sys/itpub/common/changeAppRole/lwReportEpidemicSeu/20200223030326996.do'
        header = get_header(sess, cookie_url2)
        info = get_info(sess, header)


    if info.status_code == 200:
        print('获取前一日信息成功！')
    else:
        print("获取信息失败！")
        raise
    info.encoding = 'utf-8'
    raw_info = re.search('"rows":\[\{(.*?)}', info.text).group(1)
    try:
        DZ_DQWZ = re.search('"DZ_DQWZ":"(.*?)"', raw_info).group(1)
    except:
        DZ_DQWZ = ''
    raw_info = re.sub(DZ_DQWZ, '', raw_info)
    raw_info = raw_info.split(',')

    post_key = ["NEED_CHECKIN_DATE", "DEPT_CODE", "CZR", "CZZXM", "CZRQ", "CLASS_CODE", "CLASS", "DZ_DQWZ_JD","DZ_DQWZ_WD", "DZ_DQWZ_SF", "DZ_DQWZ_CS", "DZ_DQWZ_QX", "USER_NAME_EN", "DZ_XYYYPJG_DISPLAY", "DZ_XYYYPJG", "USER_ID", "USER_NAME", "DEPT_NAME", "GENDER_CODE_DISPLAY", "GENDER_CODE", "PHONE_NUMBER", "IDCARD_NO", "LOCATION_DETAIL", "EMERGENCY_CONTACT_PERSON", "EMERGENCY_CONTACT_PHONE", "EMERGENCY_CONTACT_NATIVE", "EMERGENCY_CONTACT_HOME", "HEALTH_STATUS_CODE_DISPLAY", "HEALTH_STATUS_CODE", "HEALTH_UNSUAL_CODE", "IS_SEE_DOCTOR_DISPLAY", "IS_SEE_DOCTOR", "SAW_DOCTOR_DESC", "MEMBER_HEALTH_STATUS_CODE_DISPLAY", "MEMBER_HEALTH_STATUS_CODE", "MEMBER_HEALTH_UNSUAL_CODE", "MENTAL_STATE", "RYSFLB", "DZ_JSDTCJTW", "DZ_DTWJTW", "DZ_DTWSJCTW", "DZ_SZWZLX_DISPLAY", "DZ_SZWZLX", "DZ_SZWZ_GJ_DISPLAY", "DZ_SZWZ_GJ", "DZ_SZWZXX", "DZ_MQZNJWZ", "DZ_SZXQ_DISPLAY", "DZ_SZXQ", "LOCATION_PROVINCE_CODE_DISPLAY", "LOCATION_PROVINCE_CODE", "LOCATION_CITY_CODE_DISPLAY", "LOCATION_CITY_CODE", "LOCATION_COUNTY_CODE_DISPLAY", "LOCATION_COUNTY_CODE", "DZ_SFGL_DISPLAY", "DZ_SFGL", "DZ_WD", "DZ_GLKSSJ", "DZ_GLJSSJ", "DZ_GLDQ_DISPLAY", "DZ_GLDQ", "DZ_GLDSF_DISPLAY", "DZ_GLDSF", "DZ_GLDCS_DISPLAY", "DZ_GLDCS", "DZ_GLSZDQ", "DZ_MQSFWYSBL_DISPLAY", "DZ_MQSFWYSBL", "DZ_YSGLJZSJ", "DZ_YS_GLJZDSF_DISPLAY", "DZ_YS_GLJZDSF", "DZ_YS_GLJZDCS_DISPLAY", "DZ_YS_GLJZDCS", "DZ_MQSFWQRBL_DISPLAY", "DZ_MQSFWQRBL", "DZ_QZGLJZSJ", "DZ_QZ_GLJZDSF_DISPLAY", "DZ_QZ_GLJZDSF", "DZ_QZ_GLJZDCS_DISPLAY", "DZ_QZ_GLJZDCS", "DZ_SFYJCS1_DISPLAY", "DZ_SFYJCS1", "DZ_ZHLKRQ", "DZ_SFYJCS2_DISPLAY", "DZ_SFYJCS2", "DZ_GRYGLSJ1", "DZ_ZHJCGRYSJ1", "DZ_SFYJCS3_DISPLAY", "DZ_SFYJCS3", "DZ_ZHJCGRYSJ2", "DZ_SFYJCS4_DISPLAY", "DZ_SFYJCS4", "DZ_JJXFBSJ", "DZ_JJXFBD_SF_DISPLAY", "DZ_JJXFBD_SF", "DZ_JJXFBD_CS_DISPLAY", "DZ_JJXFBD_CS", "DZ_BRYWYXFH_DISPLAY", "DZ_BRYWYXFH", "DZ_JCQKSM", "DZ_JRSFFS_DISPLAY", "DZ_JRSFFS", "DZ_TWDS", "DZ_JRSTZK_DISPLAY", "DZ_JRSTZK", "DZ_SMJTQK", "DZ_SFYJCS5_DISPLAY", "DZ_SFYJCS5", "DZ_YJZCDDGNRQ", "DZ_SFYJCS7_DISPLAY", "DZ_SFYJCS7", "DZ_ZHJCGGRYSJ", "DZ_SFYJCS8_DISPLAY", "DZ_SFYJCS8", "DZ_JTQY_DISPLAY", "DZ_JTQY", "DZ_SFYJCS9_DISPLAY", "DZ_SFYJCS9", "DZ_YWQTXGQK_DISPLAY", "DZ_YWQTXGQK", "DZ_QKSM", "DZ_JRSFYXC_DISPLAY", "DZ_JRSFYXC", "DZ_MDDSZSF_DISPLAY", "DZ_MDDSZSF", "DZ_MDDSZCS_DISPLAY", "DZ_MDDSZCS", "DZ_JTFS_DISPLAY", "DZ_JTFS", "DZ_CCBC", "DZ_SFDXBG_DISPLAY", "DZ_SFDXBG", "DZ_SYJTGJ", "DZ_SDXQ", "REMARK", "CREATED_AT", "DZ_DBRQ", "DZ_SFYBH", "DZ_SFLXBXS", "DZ_ZDYPJG", 'DZ_SFYJCS10_DISPLAY', 'DZ_WJZYMYY', 'DZ_WJZYMYY_DISPLAY', 'DZ_SDXQ_DISPLAY', 'DZ_WJZYMQTYY', 'DZ_SFYJCS10', 'MENTAL_STATE_DISPLAY', 'HEALTH_UNSUAL_CODE_DISPLAY', 'DZ_YMJZRQ1', 'DZ_YMJZRQ2', 'MEMBER_HEALTH_UNSUAL_CODE_DISPLAY', 'DZ_SYJTGJ_DISPLAY', 'DZ_YMJZD1', 'DZ_YMJZD2']

    post_info = {}
    for info in raw_info:
        key_value = info.split(':')
        key = key_value[0].strip('"')
        val = key_value[1].strip('"')
        if key in post_key:
            if val == 'null':
                post_info[key] = ''
            else:
                post_info[key] = val

    post_info['DZ_DQWZ'] = DZ_DQWZ
    post_info['DZ_SFYBH'] = '0'
    post_info['DZ_DBRQ'] = time.strftime("%Y-%m-%d", time.localtime())
    post_info['NEED_CHECKIN_DATE'] = time.strftime("%Y-%m-%d", time.localtime())
    post_info['DZ_SFLXBXS'] = ''
    post_info['DZ_ZDYPJG'] = ''
    post_info['DZ_JSDTCJTW'] = round(random.uniform(36, 36.9), 1)

    report_url = 'http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/modules/dailyReport/T_REPORT_EPIDEMIC_CHECKIN_SAVE.do'
    report_response = sess.post(report_url, data=post_info, headers=header)
    if report_response.status_code == 200:
        print('打卡成功！')
    else:
        print("打卡失败！")


def main():
    sess = requests.session()
    try:
        username = sys.argv[1]
        password = sys.argv[2]
    except:
        username = input("一卡通号：")
        password = input("密码：")
    login(sess, username, password)
    report(sess)
    sess.close()


if __name__ == '__main__':
    main()


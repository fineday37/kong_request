import pprint
import time

import execjs
import js2py
import os
import threading
import requests

jsstr = '''    
function s(e) {
        function t(e, t) {
            return e << t | e >>> 32 - t
        }
        function n(e, t) {
            var n, r, o, i, a;
            return o = 2147483648 & e,
            i = 2147483648 & t,
            a = (1073741823 & e) + (1073741823 & t),
            (n = 1073741824 & e) & (r = 1073741824 & t) ? 2147483648 ^ a ^ o ^ i : n | r ? 1073741824 & a ? 3221225472 ^ a ^ o ^ i : 1073741824 ^ a ^ o ^ i : a ^ o ^ i
        }
        function r(e, t, n) {
            return e & t | ~e & n
        }
        function o(e, t, n) {
            return e & n | t & ~n
        }
        function i(e, t, n) {
            return e ^ t ^ n
        }
        function a(e, t, n) {
            return t ^ (e | ~n)
        }
        function s(e, o, i, a, s, l, u) {
            return e = n(e, n(n(r(o, i, a), s), u)),
            n(t(e, l), o)
        }
        function l(e, r, i, a, s, l, u) {
            return e = n(e, n(n(o(r, i, a), s), u)),
            n(t(e, l), r)
        }
        function u(e, r, o, a, s, l, u) {
            return e = n(e, n(n(i(r, o, a), s), u)),
            n(t(e, l), r)
        }
        function c(e, r, o, i, s, l, u) {
            return e = n(e, n(n(a(r, o, i), s), u)),
            n(t(e, l), r)
        }
        function p(e) {
            for (var t, n = e.length, r = n + 8, o, i = 16 * ((r - r % 64) / 64 + 1), a = new Array(i - 1), s = 0, l = 0; n > l; )
                s = l % 4 * 8,
                a[t = (l - l % 4) / 4] = a[t] | e.charCodeAt(l) << s,
                l++;
            return s = l % 4 * 8,
            a[t = (l - l % 4) / 4] = a[t] | 128 << s,
            a[i - 2] = n << 3,
            a[i - 1] = n >>> 29,
            a
        }
        function d(e) {
            var t, n, r = "", o = "";
            for (n = 0; 3 >= n; n++)
                r += (o = "0" + (t = e >>> 8 * n & 255).toString(16)).substr(o.length - 2, 2);
            return r
        }
        function f(e) {
            
            for (var t = "", n = 0; n < e.length; n++) {
                var r = e.charCodeAt(n);
                128 > r ? t += String.fromCharCode(r) : r > 127 && 2048 > r ? (t += String.fromCharCode(r >> 6 | 192),
                t += String.fromCharCode(63 & r | 128)) : (t += String.fromCharCode(r >> 12 | 224),
                t += String.fromCharCode(r >> 6 & 63 | 128),
                t += String.fromCharCode(63 & r | 128))
            }
            return t
        }
        var h, m, v, y, g, b, w, C, k, x = [], S = 7, E = 12, _ = 17, O = 22, N = 5, T = 9, M = 14, P = 20, D = 4, A = 11, R = 16, I = 23, L = 6, V = 10, F = 15, j = 21, z;
        for (x = p(e = f(e)),
        b = 1732584193,
        w = 4023233417,
        C = 2562383102,
        k = 271733878,
        h = 0; h < x.length; h += 16)
            m = b,
            v = w,
            y = C,
            g = k,
            b = s(b, w, C, k, x[h + 0], 7, 3614090360),
            k = s(k, b, w, C, x[h + 1], E, 3905402710),
            C = s(C, k, b, w, x[h + 2], _, 606105819),
            w = s(w, C, k, b, x[h + 3], O, 3250441966),
            b = s(b, w, C, k, x[h + 4], 7, 4118548399),
            k = s(k, b, w, C, x[h + 5], E, 1200080426),
            C = s(C, k, b, w, x[h + 6], _, 2821735955),
            w = s(w, C, k, b, x[h + 7], O, 4249261313),
            b = s(b, w, C, k, x[h + 8], 7, 1770035416),
            k = s(k, b, w, C, x[h + 9], E, 2336552879),
            C = s(C, k, b, w, x[h + 10], _, 4294925233),
            w = s(w, C, k, b, x[h + 11], O, 2304563134),
            b = s(b, w, C, k, x[h + 12], 7, 1804603682),
            k = s(k, b, w, C, x[h + 13], E, 4254626195),
            C = s(C, k, b, w, x[h + 14], _, 2792965006),
            b = l(b, w = s(w, C, k, b, x[h + 15], O, 1236535329), C, k, x[h + 1], 5, 4129170786),
            k = l(k, b, w, C, x[h + 6], 9, 3225465664),
            C = l(C, k, b, w, x[h + 11], M, 643717713),
            w = l(w, C, k, b, x[h + 0], P, 3921069994),
            b = l(b, w, C, k, x[h + 5], 5, 3593408605),
            k = l(k, b, w, C, x[h + 10], 9, 38016083),
            C = l(C, k, b, w, x[h + 15], M, 3634488961),
            w = l(w, C, k, b, x[h + 4], P, 3889429448),
            b = l(b, w, C, k, x[h + 9], 5, 568446438),
            k = l(k, b, w, C, x[h + 14], 9, 3275163606),
            C = l(C, k, b, w, x[h + 3], M, 4107603335),
            w = l(w, C, k, b, x[h + 8], P, 1163531501),
            b = l(b, w, C, k, x[h + 13], 5, 2850285829),
            k = l(k, b, w, C, x[h + 2], 9, 4243563512),
            C = l(C, k, b, w, x[h + 7], M, 1735328473),
            b = u(b, w = l(w, C, k, b, x[h + 12], P, 2368359562), C, k, x[h + 5], 4, 4294588738),
            k = u(k, b, w, C, x[h + 8], A, 2272392833),
            C = u(C, k, b, w, x[h + 11], R, 1839030562),
            w = u(w, C, k, b, x[h + 14], I, 4259657740),
            b = u(b, w, C, k, x[h + 1], 4, 2763975236),
            k = u(k, b, w, C, x[h + 4], A, 1272893353),
            C = u(C, k, b, w, x[h + 7], R, 4139469664),
            w = u(w, C, k, b, x[h + 10], I, 3200236656),
            b = u(b, w, C, k, x[h + 13], 4, 681279174),
            k = u(k, b, w, C, x[h + 0], A, 3936430074),
            C = u(C, k, b, w, x[h + 3], R, 3572445317),
            w = u(w, C, k, b, x[h + 6], I, 76029189),
            b = u(b, w, C, k, x[h + 9], 4, 3654602809),
            k = u(k, b, w, C, x[h + 12], A, 3873151461),
            C = u(C, k, b, w, x[h + 15], R, 530742520),
            b = c(b, w = u(w, C, k, b, x[h + 2], I, 3299628645), C, k, x[h + 0], 6, 4096336452),
            k = c(k, b, w, C, x[h + 7], V, 1126891415),
            C = c(C, k, b, w, x[h + 14], F, 2878612391),
            w = c(w, C, k, b, x[h + 5], j, 4237533241),
            b = c(b, w, C, k, x[h + 12], 6, 1700485571),
            k = c(k, b, w, C, x[h + 3], V, 2399980690),
            C = c(C, k, b, w, x[h + 10], F, 4293915773),
            w = c(w, C, k, b, x[h + 1], j, 2240044497),
            b = c(b, w, C, k, x[h + 8], 6, 1873313359),
            k = c(k, b, w, C, x[h + 15], V, 4264355552),
            C = c(C, k, b, w, x[h + 6], F, 2734768916),
            w = c(w, C, k, b, x[h + 13], j, 1309151649),
            b = c(b, w, C, k, x[h + 4], 6, 4149444226),
            k = c(k, b, w, C, x[h + 11], V, 3174756917),
            C = c(C, k, b, w, x[h + 2], F, 718787259),
            w = c(w, C, k, b, x[h + 9], j, 3951481745),
            b = n(b, m),
            w = n(w, v),
            C = n(C, y),
            k = n(k, g);
        return (d(b) + d(w) + d(C) + d(k)).toLowerCase()
    }'''
ctx = execjs.compile(jsstr)
times = time.time()
data = '{"userNick":"cntaobao世纪开元旗舰店:李虎","cid":"2271339353.1-3909439825.1#11001","userId":"2206705169056",' \
       '"cursor":1667404800000,"forward":true,"count":100,"needRecalledContent":true} '
sign_str = '52cc7bdf683833567dde40804f69148b_1667877628284' + "&" + str(int(times)) + "&" + "12574478" + "&" + data
sign = ctx.call("s", sign_str)
print(int(times))
print(sign)
appKey = "12574478"

datas = {
    "jsv": "2.6.2",
    "appKey": "12574478",
    "t": times,
    "sign": sign,
    "api": "mtop.taobao.wireless.amp2.paas.conversation.list",
    "v": "1.0",
    "type": "jsonp",
    "dataType": "jsonp",
    "callback": "mtopjsonp7",
    "data": '{"selfWwNick":null,"targetWwNick":"cntaobaotb389067134","beginDate":"20221102","endDate":"20221102"}'
}
headers = {"referer": "https://market.m.taobao.com/",
           'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'script',
           'sec-fetch-mode': 'no-cors',
           'sec-fetch-site': 'same-site',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/107.0.0.0 Safari/537.36',
           "Cookie": 'thw=cn; t=1f93bdcdc662c2e97f23e757d4acab95; _samesite_flag_=true; '
                     'cookie2=1629fb7ab88babd08d84bd74c36ea7bc; _tb_token_=7dee73eee63ee; '
                     'sgcookie=E100bYhifnv9zEsVJdMpBflRcLgVLSOuwdfI0vZi7Gaklip36HSElEdVX4dpgc2MfT1DV6xUrFMLQ93yNu'
                     '%2FLUEIQl6khHTwDaMT6wZrLPdRQASc%3D; unb=2214365765746; '
                     'sn=%E4%B8%96%E7%BA%AA%E5%BC%80%E5%85%83%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%9D%8E%E8%99%8E; '
                     'csg=794f4f7b; cancelledSubSites=empty; skt=6024394e60107b97; _cc_=U%2BGCWk%2F7og%3D%3D; '
                     'cna=A82IGtpEg2kCAXGA0sLehKwU; xlly_s=1; '
                     'uc1=cookie21=V32FPkk%2FhSg%2F&cookie14=UoeyCUjmGSfFFA%3D%3D; '
                     '_m_h5_tk=f9688f9e1593fa0f0f997874ed12f4f9_1667983331264; '
                     '_m_h5_tk_enc=3971f0e1db785762cf4b0aae207dc0b7; '
                     'tfstk=cWpfBr6u5r4jaSDgnZir7rq53GWFZMcPXxSBcqGmjQBxfp-fiQyFRipwJPWNXg1..; '
                     'l=eBg_Gi-eL9u9KAiMBO5ahurza77TmIdf51PzaNbMiInca6HPsFMZYNCUj0re'
                     '-dtjgtfxIFKzmSrNYdEB8SzLRrtVfX89a5k3axv9-; '
                     'isg=BBAQySrER_iLThp2Tqj7j9M34V5i2fQjCJwBqgrgV2s-Rbnvt-hWs8KzHQ2lkqz7'}

res = requests.get(url="https://h5api.m.taobao.com/h5/mtop.taobao.wireless.amp2.im.paas.message.list/1.0/?jsv=2.6.2"
                       "&appKey=12574478&t=1667976675927&sign=fef6f4e5cbece4e78728402c18d0902c&api=mtop.taobao"
                       ".wireless.amp2.im.paas.message.list&v=1.0&type=jsonp&dataType=jsonp&callback=mtopjsonp7&data"
                       "=%7B%22userNick%22%3A%22cntaobao%E4%B8%96%E7%BA%AA%E5%BC%80%E5%85%83%E6%97%97%E8%88%B0%E5%BA"
                       "%97%3A%E6%9D%8E%E8%99%8E%22%2C%22cid%22%3A%222207813896693.1-3909439825.1%2311001%22%2C"
                       "%22userId%22%3A%222206617619452%22%2C%22cursor%22%3A1667318400000%2C%22forward%22%3Atrue%2C"
                       "%22count%22%3A100%2C%22needRecalledContent%22%3Atrue%7D",
                   headers=headers)
pprint.pprint(res.text)

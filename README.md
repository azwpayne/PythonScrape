# MiGu登录参数破解

## 目标：破解咪咕视频登录参数（**enpassword**、**fingerPrint**、**fingerPrintDetail**）

## 工具:NodeJs + Chrome 开发者工具

## **enpassword**

### 找到登录入口：

### 查找方式：

点击登录 —> 开启chrome开发者工具 -> 重载框架 —> 抓到[登录包](https://passport.migu.cn/login?sourceid=203021&apptype=2&forceAuthn=true&isPassive=false&authType=&display=&nodeId=70027513&relayState=login&weibo=1&callbackURL=http%3A%2F%2Fwww.miguvideo.com%2Fmgs%2Fwebsite%2Fprd%2Findex.html%3FisIframe%3Dweb)

如下：

![1.登录入口查找](D:\Note\网站JS解密与逆向\MiGu\1.登录入口查找.png)

### 加密参数寻找

清空之后，使用错误的账号密码登录。一共两个包两张图片。图片开源不看，具体看包，最后在authn包中看到了我们登录所加密过的三个参数，如下

![2.加密参数寻找](D:\Note\网站JS解密与逆向\MiGu\2.加密参数寻找.png)

### 海里捞针-找参数

在搜索框(ctrl + shift + F )下搜索enpassword参数，进入source File 发现link 93，name并未加密；那么就是在它的class 属性 J_RsaPsd中。再次找！

![3.海底捞针-找参数](D:\Note\网站JS解密与逆向\MiGu\3.海底捞针-找参数.png)

### 海里捞针-找参数、埋断点

找到三个 J_RsaPsd，每个都上断点，然后在点登录一下

![3.海底捞针-找参数埋断点](D:\Note\网站JS解密与逆向\MiGu\3.海底捞针-找参数埋断点.png)

encrypt：加密函数，b.val加密对象（输入的密码）

![3.海底捞针-找参数埋断点1](D:\Note\网站JS解密与逆向\MiGu\3.海底捞针-找参数埋断点1.png)

将其扣出来！

为什么扣这里？因为这里为加密处！由明文转为密文。那我们拿到这些就以为着拿到了加密的函数。就可以自己实现加密

>  c = new p.RSAKey;
>                             c.setPublic(a.result.modulus, a.result.publicExponent);
>                             var d = c.encrypt(b.val());

该写如下：（js丫）

```javascript
function getPwd(pwd) {
    c = new p.RSAKey;
    c.setPublic(a.result.modulus, a.result.publicExponent);
    var d = c.encrypt(b.val());
    return d;
}
```

虽然我们加密的函数已经找到了，but，我们是在自己的环境下并不一定有这个函数（c.encrypt）。所以现在需要去找c.encrypt

![4.袖里寻针-尝试自己完成加密](D:\Note\网站JS解密与逆向\MiGu\4.袖里寻针-尝试自己完成加密.png)

新问题：p.RSAKey；没有定义；回到chrome进入p.RSAKey-（选中点击进入f db()）

![4.袖里寻针-尝试自己完成加密-方法p.RSAKey](D:\Note\网站JS解密与逆向\MiGu\4.袖里寻针-尝试自己完成加密-方法p.RSAKey.png)



进入f db（）扣出这个方法，然后改写

寻找a.result.modulus, a.result.publicExponent两个参数，

其实是publickey包返回的结果那么至此**enpassword**加密完成

补两个环境参数

```js
window = this;
navigator = {};
```

![5.加密破解完成](D:\Note\网站JS解密与逆向\MiGu\5.加密破解完成.png)

## **fingerPrint**、**fingerPrintDetail**参数破解

![6.换汤不换药-继续](D:\Note\网站JS解密与逆向\MiGu\6.换汤不换药-继续.png)

link480 下断点点击下一步，运行

**运行一步**, 进入**RSAfingerPrint**函数内，把o.page.RSAfingerPrint方法抠出来

在页面中观察a，b参数

![6.换汤不换药-扣取+查看参数](D:\Note\网站JS解密与逆向\MiGu\6.换汤不换药-扣取+查看参数.png)

观察发现：

其实a，b，就是我们的**a.result.modulus, a.result.publicExponent**，

```js
rsaFingerprint = function () {
    a = "00833c4af965ff7a8409f8b5d5a83d87f2f19d7c1eb40dc59a98d2346cbb145046b2c6facc25b5cc363443f0f7ebd9524b7c1e1917bf7d849212339f6c1d3711b115ecb20f0c89fc2182a985ea28cbb4adf6a321ff7e715ba9b8d7261d1c140485df3b705247a70c28c9068caabbedbf9510dada6d13d99e57642b853a73406817";
    b = "010001";
    var c = $.fingerprint.details
        , d = $.fingerprint.result
        , e = c.length
        , f = ""
        , g = new m.RSAKey;
    console.log(a, b)
    g.setPublic(a, b);
    for (var h = g.encrypt(d), i = 0; e > i; i += 117)
        f += g.encrypt(c.substr(i, 117));
    return {
        details: f,
        result: h
    }
}
rsaFingerprint()
```

继续寻找；这两个

```
c = $.fingerprint.details 
d = $.fingerprint.result
```

浏览器里面测一下，把他从console拿出来

![6.完成](D:\Note\网站JS解密与逆向\MiGu\6.完成.png)

![7.完成](D:\Note\网站JS解密与逆向\MiGu\7.完成.png)
# qimingpian接口加密分析

工具：Chrome + NodeJS + Pycharm

点击获取结果

## 抓包

调出开发者工具，直接到xhr(这里点击改变的时候并未发生网址变更、所以这是Ajax)

## 参数寻找

一共就两个包，但Preview里面没有数据，but几KB的包没有鬼？反正我不相信![1.参数寻找](D:\Note\网站JS解密与逆向\qimingpian\1.参数寻找.png)

### 追根揭底

直接把encrypt_data，拉出来全局搜索（ctrl + shift + F），encrypt_data参数一共六个，但就只有这一个最可疑（我就是不告诉你为什么。。。），其实你看看周围的函数你就会发现，TmD一个个返回啥呀，不是错误就是上传失败。封IP的信息就放了。怕了怕了

![2.有猫腻](D:\Note\网站JS解密与逆向\qimingpian\2.有猫腻.png)

在console里面打印一下Object(u.a)(e.encrypt_data)

初一看，好像是又好像不是（仅有部分信息）

> 只有标题，为什么没信息呢？
>
> 我告诉你为什么，因为数据被加密了，只给你看标题，充钱就给你看。
>
> 不慌，不慌。那个xx说过我离成功就一步了

点击 下一步![next](D:\Note\网站JS解密与逆向\qimingpian\next.png)没错，就是它。老板，求解密一下？

ok，感谢老板。再次在console里面打印一下Object(u.a)(e.encrypt_data)

当当当~

![2.3有猫腻-揭开神秘面纱](D:\Note\网站JS解密与逆向\qimingpian\2.3有猫腻-揭开神秘面纱.png)

ok，那它是怎么来的呢？

> 都晓得它是这里解密出来的，还不就进去搞他呗

![3.紧随其后](D:\Note\网站JS解密与逆向\qimingpian\3.紧随其后.png)

当当当~，扣它，把这个函数扣出来（快到我怀里来~）

![3.紧随其后-加密参数](D:\Note\网站JS解密与逆向\qimingpian\3.紧随其后-加密参数.png)

到这里就基本上把主函数弄完了，但是还没有完

a.a.decode(t)这个鬼我们还不晓得，进去找他，扣它

![4.缺啥补啥](D:\Note\网站JS解密与逆向\qimingpian\4.缺啥补啥.png)

```
decode = function (t) {
    var e = (t = String(t).replace(f, "")).length;
    e % 4 == 0 && (e = (t = t.replace(/==?$/, "")).length),
    (e % 4 == 1 || /[^+a-zA-Z0-9/]/.test(t)) && l("Invalid character: the string to be decoded is not correctly encoded.");
    for (var n, r, i = 0, o = "", a = -1; ++a < e;)
        r = c.indexOf(t.charAt(a)),
            n = i % 4 ? 64 * n + r : r,
        i++ % 4 && (o += String.fromCharCode(255 & n >> (-2 * i & 6)));
    return o
},

function o(t) {
    return JSON.parse(s("5e5062e82f15fe4ca9d24bc5", a.a.decode(t), 0, 0, "012345677890123", 1))
}
```

这里的参数t，还不晓得，既然是外面传进来的，那么它要么是js生成的，要么就是全局的。全前面找，去console里面测一下，测多次。如果是不变的那么它就是一个全局参数。

拿过来就好，然后在console里面copy（t）。

同理，参数c，和f也是

但是c， 和f 就在decode函数前面，拿了就好

![4.over](D:\Note\网站JS解密与逆向\qimingpian\4.over.png)

完成！

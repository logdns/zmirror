# coding=utf-8
import re
from config import *
from EasyWebsiteMirror import regex_adv_url_rewriter, regex_url_reassemble, \
    static_file_extensions_list, external_domains_set, allowed_domains_set, myurl_prefix, cdn_domains_number, \
    static_file_extensions_list
import EasyWebsiteMirror
from urllib.parse import urljoin
from ColorfulPyPrint import *

test_cases = (
    (
        'background: url(../images/boardsearch/mso-hd.gif);',
        'background: url(/some23333_/images/boardsearch/mso-hd.gif);'
    ),
    (
        'background: url(http://www.google.com/images/boardsearch/mso-hd.gif););',
        'background: url(/extdomains/https-www.google.com/images/boardsearch/mso-hd.gif););'
    ),
    (
        ": url('http://www.google.com/images/boardsearch/mso-hd.gif');",
        ": url('/extdomains/https-www.google.com/images/boardsearch/mso-hd.gif');"
    ),
    (
        'background: url("//www.google.com/images/boardsearch/mso-hd.gif");',
        'background: url("/extdomains/https-www.google.com/images/boardsearch/mso-hd.gif");'
    ),
    (
        r"""background: url ( "//www.google.com/images/boardsearch/mso-hd.gif" );""",
        r"""background: url ( "/extdomains/https-www.google.com/images/boardsearch/mso-hd.gif" );"""
    ),
    (
        r""" src="https://ssl.gstatic.com/233.jpg" """,
        r""" src="/extdomains/https-ssl.gstatic.com/233.jpg" """
    ),
    (
        r"""href="http://ssl.gstatic.com/233.jpg" """,
        r"""href="/extdomains/https-ssl.gstatic.com/233.jpg" """
    ),
    (
        r"""background: url("//ssl.gstatic.com/images/boardsearch/mso-hd.gif"); """,
        r"""background: url("/extdomains/https-ssl.gstatic.com/images/boardsearch/mso-hd.gif"); """
    ),
    (
        r"""background: url ( "//ssl.gstatic.com/images/boardsearch/mso-hd.gif" ); """,
        r"""background: url ( "/extdomains/https-ssl.gstatic.com/images/boardsearch/mso-hd.gif" ); """
    ),
    (
        r"""src="http://www.google.com/233.jpg" """,
        r"""src="/extdomains/https-www.google.com/233.jpg" """
    ),
    (
        r"""href="http://www.google.com/233.jpg" """,
        r"""href="/extdomains/https-www.google.com/233.jpg" """,
    ),
    (
        r"""href="https://www.foo.com/233.jpg" """,
        r"""href="https://www.foo.com/233.jpg" """,
    ),
    (
        r"""xhref="http://www.google.com/233.jpg" """,
        r"""xhref="http://www.google.com/233.jpg" """,
    ),
    (
        r"""s.href="http://www.google.com/path/233.jpg" """,
        r"""s.href="/extdomains/https-www.google.com/path/233.jpg" """,
    ),
    (
        r"""background: url(../images/boardsearch/mso-hd.gif?a=x&bb=fr%34fd);""",
        r"""background: url(/some23333_/images/boardsearch/mso-hd.gif?a=x&bb=fr%34fd);""",
    ),
    (
        r"""background: url(http://www.google.com/images/boardsearch/mso-hd.gif?a=x&bb=fr%34fd);""",
        r"""background: url(/extdomains/https-www.google.com/images/boardsearch/mso-hd.gif?a=x&bb=fr%34fd);""",
    ),
    (
        r"""src="http://ssl.gstatic.com/233.jpg?a=x&bb=fr%34fd" """,
        r"""src="/extdomains/https-ssl.gstatic.com/233.jpg?a=x&bb=fr%34fd" """,
    ),
    (
        r"""href="index.php/img/233.jx" """,
        r"""href="/some23333_/url/index.php/img/233.jx" """,
    ),
    (
        r"""href="/img/233.jss" """,
        r"""href="/img/233.jss" """,
    ),
    (
        r"""href="img/233.jpg" """,
        r"""href="/some23333_/url/img/233.jpg" """,
    ),
    (
        r"""nd-image:url(/static/images/project-logos/zhwiki.png)}@media""",
        r"""nd-image:url(/static/images/project-logos/zhwiki.png)}@media""",
    ),
    (
        r"""nd-image:url(static/images/project-logos/zhwiki.png)}@media""",
        r"""nd-image:url(/some23333_/url/static/images/project-logos/zhwiki.png)}@media""",
    ),
    (
        r"""@import "/wikipedia/zh/w/index.php?title=MediaWiki:Gadget-fontsize.css&action=raw&ctype=text/css";""",
        r"""@import "/wikipedia/zh/w/index.php?title=MediaWiki:Gadget-fontsize.css&action=raw&ctype=text/css";""",
    ),
    (
        r"""(window['gbar']=window['gbar']||{})._CONFIG=[[[0,"www.gstatic.com","og.og2.en_US.8UP-Hyjzcx8.O","com","zh-CN","1",0,[3,2,".40.64.","","1300102,3700275,3700388","1461637855","0"],"40400","LJ8qV4WxEI_QjwOio6SoDw",0,0,"og.og2.w5jrmmcgm1gp.L.F4.O","AA2YrTt48BbbcLnincZsbUECyYqIio-xhw","AA2YrTu9IQdyFrx2T9b82QPSt9PVPEWOIw","",2,0,200,"USA"],null,0,["m;/_/scs/abc-static/_/js/k=gapi.gapi.en.CqFrPIKIxF4.O/m=__features__/rt=j/d=1/rs=AHpOoo_SqGYjlKSpzsbc2UGyTC5n3Z0ZtQ","https://apis.google.com","","","","",null,1,"es_plusone_gc_20160421.0_p0","zh-CN"],["1","gci_91f30755d6a6b787dcc2a4062e6e9824.js","googleapis.client:plusone:gapi.iframes","","zh-CN"],null,null,null,[0.009999999776482582,"com","1",[null,"","w",null,1,5184000,1,0,""],null,[["","","",0,0,-1]],[null,0,0],0,null,null,["5061451","google\\.(com|ru|ca|by|kz|com\\.mx|com\\.tr)$",1]],null,[0,0,0,null,"","","",""],[1,0.001000000047497451,1],[1,0.1000000014901161,2,1],[0,"",null,"",0,"加载您的 Marketplace 应用时出错。","您没有任何 Marketplace 应用。",0,[1,"https://www.google.com/webhp?tab=ww","搜索","","0 -276px",null,0],null,null,1,0],[1],[0,1,["lg"],1,["lat"]],[["","","","","","","","","","","","","","","","","","","","def","","","","","",""],[""]],null,null,null,[30,127,1,0,60],null,null,null,null,null,[1,1]]];(window['gbar']=window['gbar']||{})._LDD=["in","fot"];this.gbar_=this.gbar_||{};(function(_){var window=this;""",
        r"""(window['gbar']=window['gbar']||{})._CONFIG=[[[0,"www.gstatic.com","og.og2.en_US.8UP-Hyjzcx8.O","com","zh-CN","1",0,[3,2,".40.64.","","1300102,3700275,3700388","1461637855","0"],"40400","LJ8qV4WxEI_QjwOio6SoDw",0,0,"og.og2.w5jrmmcgm1gp.L.F4.O","AA2YrTt48BbbcLnincZsbUECyYqIio-xhw","AA2YrTu9IQdyFrx2T9b82QPSt9PVPEWOIw","",2,0,200,"USA"],null,0,["m;/_/scs/abc-static/_/js/k=gapi.gapi.en.CqFrPIKIxF4.O/m=__features__/rt=j/d=1/rs=AHpOoo_SqGYjlKSpzsbc2UGyTC5n3Z0ZtQ","https://apis.google.com","","","","",null,1,"es_plusone_gc_20160421.0_p0","zh-CN"],["1","gci_91f30755d6a6b787dcc2a4062e6e9824.js","googleapis.client:plusone:gapi.iframes","","zh-CN"],null,null,null,[0.009999999776482582,"com","1",[null,"","w",null,1,5184000,1,0,""],null,[["","","",0,0,-1]],[null,0,0],0,null,null,["5061451","google\\.(com|ru|ca|by|kz|com\\.mx|com\\.tr)$",1]],null,[0,0,0,null,"","","",""],[1,0.001000000047497451,1],[1,0.1000000014901161,2,1],[0,"",null,"",0,"加载您的 Marketplace 应用时出错。","您没有任何 Marketplace 应用。",0,[1,"https://www.google.com/webhp?tab=ww","搜索","","0 -276px",null,0],null,null,1,0],[1],[0,1,["lg"],1,["lat"]],[["","","","","","","","","","","","","","","","","","","","def","","","","","",""],[""]],null,null,null,[30,127,1,0,60],null,null,null,null,null,[1,1]]];(window['gbar']=window['gbar']||{})._LDD=["in","fot"];this.gbar_=this.gbar_||{};(function(_){var window=this;""",
    ),
    (
        r""" src="" """,
        r""" src="" """,
    ),
    (
        r""" this.src=c; """,
        r""" this.src=c; """,
    ),
    (
        r""" href="http://www.google.com/" """,
        r""" href="/extdomains/https-www.google.com/" """,
    ),
    (
        r"""_.Gd=function(a){if(_.na(a)||!a||a.Gb)return!1;var c=a.src;if(_.nd(c))return c.uc(a);var d=a.type,e=a.b;c.removeEventListener?c.removeEventListener(d,e,a.fc):c.detachEvent&&c.detachEvent(Cd(d),e);xd--;(d=_.Ad(c))?(td(d,a),0==d.o&&(d.src=null,c[vd]=null)):qd(a);return!0};Cd=function(a){return a in wd?wd[a]:wd[a]="on"+a};Id=function(a,c,d,e){var f=!0;if(a=_.Ad(a))if(c=a.b[c.toString()])for(c=c.concat(),a=0;a<c.length;a++){var g=c[a];g&&g.fc==d&&!g.Gb&&(g=Hd(g,e),f=f&&!1!==g)}return f};""",
        r"""_.Gd=function(a){if(_.na(a)||!a||a.Gb)return!1;var c=a.src;if(_.nd(c))return c.uc(a);var d=a.type,e=a.b;c.removeEventListener?c.removeEventListener(d,e,a.fc):c.detachEvent&&c.detachEvent(Cd(d),e);xd--;(d=_.Ad(c))?(td(d,a),0==d.o&&(d.src=null,c[vd]=null)):qd(a);return!0};Cd=function(a){return a in wd?wd[a]:wd[a]="on"+a};Id=function(a,c,d,e){var f=!0;if(a=_.Ad(a))if(c=a.b[c.toString()])for(c=c.concat(),a=0;a<c.length;a++){var g=c[a];g&&g.fc==d&&!g.Gb&&(g=Hd(g,e),f=f&&!1!==g)}return f};""",
    ),
    (
        r"""<script>(function(){window.google={kEI:'wZ4qV6KnMtjwjwOztI2ABQ',kEXPI:'10201868',authuser:0,j:{en:1,bv:24,u:'e4f4906d',qbp:0},kscs:'e4f4906d_24'};google.kHL='zh-CN';})();(function(){google.lc=[];google.li=0;google.getEI=function(a){for(var b;a&&(!a.getAttribute||!(b=a.getAttribute("eid")));)a=a.parentNode;return b||google.kEI};google.getLEI=function(a){for(var b=null;a&&(!a.getAttribute||!(b=a.getAttribute("leid")));)a=a.parentNode;return b};google.https=function(){return"https:"==window.location.protocol};google.ml=function(){return null};google.wl=function(a,b){try{google.ml(Error(a),!1,b)}catch(c){}};google.time=function(){return(new Date).getTime()};google.log=function(a,b,c,e,g){a=google.logUrl(a,b,c,e,g);if(""!=a){b=new Image;var d=google.lc,f=google.li;d[f]=b;b.onerror=b.onload=b.onabort=function(){delete d[f]};window.google&&window.google.vel&&window.google.vel.lu&&window.google.vel.lu(a);b.src=a;google.li=f+1}};google.logUrl=function(a,b,c,e,g){var d="",f=google.ls||"";if(!c&&-1==b.search("&ei=")){var h=google.getEI(e),d="&ei="+h;-1==b.search("&lei=")&&((e=google.getLEI(e))?d+="&lei="+e:h!=google.kEI&&(d+="&lei="+google.kEI))}a=c||"/"+(g||"gen_204")+"?atyp=i&ct="+a+"&cad="+b+d+f+"&zx="+google.time();/^http:/i.test(a)&&google.https()&&(google.ml(Error("a"),!1,{src:a,glmm:1}),a="");return a};google.y={};google.x=function(a,b){google.y[a.id]=[a,b];return!1};google.load=function(a,b,c){google.x({id:a+k++},function(){google.load(a,b,c)})};var k=0;})();""",
        r"""<script>(function(){window.google={kEI:'wZ4qV6KnMtjwjwOztI2ABQ',kEXPI:'10201868',authuser:0,j:{en:1,bv:24,u:'e4f4906d',qbp:0},kscs:'e4f4906d_24'};google.kHL='zh-CN';})();(function(){google.lc=[];google.li=0;google.getEI=function(a){for(var b;a&&(!a.getAttribute||!(b=a.getAttribute("eid")));)a=a.parentNode;return b||google.kEI};google.getLEI=function(a){for(var b=null;a&&(!a.getAttribute||!(b=a.getAttribute("leid")));)a=a.parentNode;return b};google.https=function(){return"https:"==window.location.protocol};google.ml=function(){return null};google.wl=function(a,b){try{google.ml(Error(a),!1,b)}catch(c){}};google.time=function(){return(new Date).getTime()};google.log=function(a,b,c,e,g){a=google.logUrl(a,b,c,e,g);if(""!=a){b=new Image;var d=google.lc,f=google.li;d[f]=b;b.onerror=b.onload=b.onabort=function(){delete d[f]};window.google&&window.google.vel&&window.google.vel.lu&&window.google.vel.lu(a);b.src=a;google.li=f+1}};google.logUrl=function(a,b,c,e,g){var d="",f=google.ls||"";if(!c&&-1==b.search("&ei=")){var h=google.getEI(e),d="&ei="+h;-1==b.search("&lei=")&&((e=google.getLEI(e))?d+="&lei="+e:h!=google.kEI&&(d+="&lei="+google.kEI))}a=c||"/"+(g||"gen_204")+"?atyp=i&ct="+a+"&cad="+b+d+f+"&zx="+google.time();/^http:/i.test(a)&&google.https()&&(google.ml(Error("a"),!1,{src:a,glmm:1}),a="");return a};google.y={};google.x=function(a,b){google.y[a.id]=[a,b];return!1};google.load=function(a,b,c){google.x({id:a+k++},function(){google.load(a,b,c)})};var k=0;})();""",
    ),
    (
        r"""background-image: url("../skin/default/tabs_m_tile.gif");""",
        r"""background-image: url("/some23333_/skin/default/tabs_m_tile.gif");""",
    ),
    (
        r"""background-image: url("xx/skin/default/tabs_m_tile.gif");""",
        r"""background-image: url("/some23333_/url/xx/skin/default/tabs_m_tile.gif");""",
    ),
    (
        r"""} else 2 == e ? this.Ea ? this.Ea.style.display = "" : (e = QS_XA("sbsb_j " + this.$.ef), f = QS_WA("a"), f.id = "sbsb_f", f.href = "http://www.google.com/support/websearch/bin/answer.py?hl=" + this.$.Xe + "&answer=106230", f.innerHTML = this.$.$k, e.appendChild(f), e.onmousedown = QS_c(this.Ia, this), this.Ea = e, this.ma.appendChild(this.Ea)) : 3 == e ? (e = this.cf.pop(), e || (e = QS_WA("li"), e.VLa = !0, f = QS_WA("div", "sbsb_e"), e.appendChild(f)), this.qa.appendChild(e)) : QS_rhb(this, e) &&""",
        r"""} else 2 == e ? this.Ea ? this.Ea.style.display = "" : (e = QS_XA("sbsb_j " + this.$.ef), f = QS_WA("a"), f.id = "sbsb_f", f.href = "/extdomains/https-www.google.com/support/websearch/bin/answer.py?hl=" + this.$.Xe + "&answer=106230", f.innerHTML = this.$.$k, e.appendChild(f), e.onmousedown = QS_c(this.Ia, this), this.Ea = e, this.ma.appendChild(this.Ea)) : 3 == e ? (e = this.cf.pop(), e || (e = QS_WA("li"), e.VLa = !0, f = QS_WA("div", "sbsb_e"), e.appendChild(f)), this.qa.appendChild(e)) : QS_rhb(this, e) &&""",
    ),
    (
        r"""m.background = "url(" + f + ") no-repeat " + b.Ea""",
        r"""m.background = "url(" + f + ") no-repeat " + b.Ea""",
    ),
    (
        r"""m.background="url("+f+") no-repeat " + b.Ea""",
        r"""m.background="url("+f+") no-repeat " + b.Ea""",
    ),
    (
        r""" "assetsBasePath" : "https:\/\/encrypted-tbn0.gstatic.com\/a\/1462524371\/", """,
        r""" "assetsBasePath" : "\/extdomains\/https-encrypted-tbn0.gstatic.com\/a\/1462524371\/", """
    ),
    (
        r""" " fullName" : "\/i\/start\/Aploium", """,
        r""" " fullName" : "\/i\/start\/Aploium", """
    ),
    (
        r"""!0,g=g.replace(/location\.href/gi,QS_qga(l))),e.push(g);if(0<e.length){f=e.join(";");f=f.replace(/,"is":_loc/g,"");f=f.replace(/,"ss":_ss/g,"");f=f.replace(/,"fp":fp/g,"");f=f.replace(/,"r":dr/g,"");try{var t=QS_Mla(f)}catch(w){f=w.EC,e={},f&&(e.EC=f.substr(0,200)),QS_Lla(k,c,"P",e)}try{ba=b.ha,QS_hka(t,ba)}catch(w){QS_Lla(k,c,"X")}}if(d)c=a.lastIndexOf("\x3c/script>"),b.$=0>c?a:a.substr(c+9);else if('"NCSR"'==a)return QS_Lla(k,c,"C"),!1;return!0};""",
        r"""!0,g=g.replace(/location\.href/gi,QS_qga(l))),e.push(g);if(0<e.length){f=e.join(";");f=f.replace(/,"is":_loc/g,"");f=f.replace(/,"ss":_ss/g,"");f=f.replace(/,"fp":fp/g,"");f=f.replace(/,"r":dr/g,"");try{var t=QS_Mla(f)}catch(w){f=w.EC,e={},f&&(e.EC=f.substr(0,200)),QS_Lla(k,c,"P",e)}try{ba=b.ha,QS_hka(t,ba)}catch(w){QS_Lla(k,c,"X")}}if(d)c=a.lastIndexOf("\x3c/script>"),b.$=0>c?a:a.substr(c+9);else if('"NCSR"'==a)return QS_Lla(k,c,"C"),!1;return!0};"""
    )
)


current_path = "/some23333_/url/"


class DbgRequest:
    path = current_path


EasyWebsiteMirror.set_request_for_debug(DbgRequest)

ColorfulPyPrint_set_verbose_level(5)
fail_count = 0

for resp_text, correct in test_cases:

    resp_text_raw = resp_text
    resp_text = regex_adv_url_rewriter.sub(regex_url_reassemble, resp_text)
    if resp_text != correct:
        errprint('\nRAW:      ', resp_text_raw, '\nRESULT:   ', resp_text, '\nCORRECT:  ', correct)
        fail_count += 1


if not fail_count:
    infoprint('All', len(test_cases), 'tests passed')
else:
    errprint('Failed in ', fail_count, 'tests')
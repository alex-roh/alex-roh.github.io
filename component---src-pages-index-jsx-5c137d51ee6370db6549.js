(window.webpackJsonp=window.webpackJsonp||[]).push([[9],{"3WF5":function(e,t,n){var a=n("eUgh"),o=n("ut/Y"),i=n("l9OW"),l=n("Z0cm");e.exports=function(e,t){return(l(e)?a:i)(e,o(t,3))}},Dtc0:function(e,t,n){"use strict";n.r(t);var a=n("xweI"),o=n.n(a),i=n("q1tI"),l=n.n(i),r=n("ntAx"),c=n("DGZL"),s=n("bSql"),m=n("PZY4"),d=n("3WF5"),u=n.n(d),p=n("vOnD"),g=n("Wbzz"),f=p.d.div.withConfig({displayName:"SideTagList__RelativeWrapper",componentId:"sc-11pn9fc-0"})(["position:relative;"]),h=p.d.aside.withConfig({displayName:"SideTagList__Wrapper",componentId:"sc-11pn9fc-1"})(["position:absolute;left:112%;top:0px;width:200px;height:100px;font-size:16px;@media (max-width:1300px){display:none;}"]),x=p.d.div.withConfig({displayName:"SideTagList__Title",componentId:"sc-11pn9fc-2"})(["margin-bottom:25px;font-weight:bold;color:",";"],(function(e){return e.theme.colors.secondaryText})),E=p.d.li.withConfig({displayName:"SideTagList__Tag",componentId:"sc-11pn9fc-3"})(["margin-bottom:16px;color:",";cursor:pointer;transition:color 0.3s;&:hover{color:",";}& > a{color:inherit;text-decoration:none;}"],(function(e){return e.theme.colors.tertiaryText}),(function(e){return e.theme.colors.text})),k=function(e){var t=e.tags,n=e.postCount;return l.a.createElement(f,null,l.a.createElement(h,null,l.a.createElement(x,null,"TAG LIST"),l.a.createElement("ul",null,l.a.createElement(E,null,l.a.createElement(g.Link,{to:"/tags"},"all (",n,")")),u()(t,(function(e){return l.a.createElement(E,null,l.a.createElement(g.Link,{to:"/tags?q="+e.fieldValue},e.fieldValue," (",e.totalCount,")"))})))))},v=n("XUsr"),w=n("mpmw"),b=n("C4nX");t.default=function(e){var t=e.data,n=t.allMarkdownRemark.nodes,a=o()(t.allMarkdownRemark.group,["totalCount"]).reverse();return 0===n.length?l.a.createElement("p",null,'No blog posts found. Add markdown posts to "content/blog" (or the directory you specified for the "gatsby-source-filesystem" plugin in gatsby-config.js).'):l.a.createElement(r.a,null,l.a.createElement(c.a,{title:b.title,description:b.description,url:b.siteUrl}),l.a.createElement(w.a,{size:48}),l.a.createElement(s.a,null),l.a.createElement(v.a,null),l.a.createElement(k,{tags:a,postCount:n.length}),l.a.createElement(m.a,{postList:n}))}},GxtF:function(e,t,n){"use strict";var a=n("q1tI"),o=n.n(a),i=n("vOnD"),l=n("Wbzz"),r=i.d.div.withConfig({displayName:"TagList__TagListWrapper",componentId:"sc-s1uz5f-0"})(["margin-bottom:16px;word-break:break-all;"]),c=i.d.div.withConfig({displayName:"TagList__TagLink",componentId:"sc-s1uz5f-1"})(["display:inline-block;padding:9.6px 11.2px;margin-right:8px;margin-bottom:8px;border-radius:50px;background-color:",";color:",";text-decoration:none;font-size:14.4px;transition:all 0.2s;&:hover{background-color:",";}"],(function(e){return e.selected?e.theme.colors.selectedTagBackground:e.theme.colors.tagBackground}),(function(e){return e.selected?e.theme.colors.selectedTagText:e.theme.colors.tagText}),(function(e){return e.selected?e.theme.colors.hoveredSelectedTagBackground:e.theme.colors.hoveredTagBackground})),s=function(e){return e.replace(/\s+/g,"-")};t.a=function(e){var t=e.tagList,n=e.count,a=e.selected;return t?n?o.a.createElement(r,null,t.map((function(e,t){return o.a.createElement(l.Link,{key:JSON.stringify({tag:e,i:t}),to:a===e.fieldValue?"/tags":"/tags?q="+e.fieldValue},o.a.createElement(c,{selected:e.fieldValue===a},s(e.fieldValue)," (",e.totalCount,")"))}))):o.a.createElement(r,null,t.map((function(e,t){return o.a.createElement(l.Link,{key:JSON.stringify({tag:e,i:t}),to:"/tags?q="+e},o.a.createElement(c,null,s(e)))}))):null}},PZY4:function(e,t,n){"use strict";var a=n("DzJC"),o=n.n(a),i=n("q1tI"),l=n.n(i),r=n("vOnD"),c=n("Wbzz"),s=n("PyCY"),m=n("XUsr"),d=n("GxtF"),u=r.d.div.withConfig({displayName:"PostList__PostListWrapper",componentId:"sc-1oqnm6-0"})(["@media (max-width:768px){padding:0 10px;}"]),p=r.d.div.withConfig({displayName:"PostList__PostWrapper",componentId:"sc-1oqnm6-1"})(["position:relative;top:0;transition:all 0.5s;@media (max-width:768px){padding:0 5px;}"]),g=r.d.p.withConfig({displayName:"PostList__Date",componentId:"sc-1oqnm6-2"})(["margin-bottom:16px;font-size:14.4px;color:",";"],(function(e){return e.theme.colors.tertiaryText})),f=r.d.p.withConfig({displayName:"PostList__Excerpt",componentId:"sc-1oqnm6-3"})(["margin-bottom:32px;line-height:1.7;font-size:16px;color:",";word-break:break-all;"],(function(e){return e.theme.colors.secondaryText}));t.a=function(e){var t=e.postList,n=Object(i.useState)(10),a=n[0],r=n[1],h=o()((function(){document.documentElement.scrollHeight-document.documentElement.scrollTop<=document.documentElement.clientHeight+100&&a<t.length&&setTimeout((function(){return r(a+10)}),300)}),250);return Object(i.useEffect)((function(){return window.addEventListener("scroll",h),function(){window.removeEventListener("scroll",h)}}),[a,t]),Object(i.useEffect)((function(){r(10)}),[t]),l.a.createElement(u,null,t.slice(0,a).map((function(e,n){var o=e.frontmatter,i=o.title,r=o.date,u=o.tags,h=e.excerpt,x=e.fields.slug;return l.a.createElement(l.a.Fragment,null,l.a.createElement(p,null,l.a.createElement(s.a,{size:"bg"},l.a.createElement(c.Link,{to:x},i)),l.a.createElement(g,null,r),l.a.createElement(f,null,h),l.a.createElement(d.a,{tagList:u})),a-1!==n&&t.length-1!==n&&l.a.createElement(m.a,{mt:"48px",mb:"32px"}))})))}},bSql:function(e,t,n){"use strict";var a=n("q1tI"),o=n.n(a),i=n("vOnD"),l=n("ma3e"),r=n("C4nX"),c=i.d.div.withConfig({displayName:"Bio__BioWrapper",componentId:"sc-5v8ml6-0"})(["display:flex;align-items:center;@media (max-width:768px){padding:0 15px;}"]),s="undefined"!=typeof window&&"localhost:8000"===window.location.host?"http://localhost:8000":r.siteUrl,m=i.d.div.withConfig({displayName:"Bio__Profile",componentId:"sc-5v8ml6-1"})(["flex:0 0 auto;margin-right:16px;width:128px;height:128px;border-radius:999px;background-image:url(","/profile.gif);background-size:cover;background-position:center;"],s),d=i.d.div.withConfig({displayName:"Bio__Author",componentId:"sc-5v8ml6-2"})(["margin-bottom:4.8px;font-size:24px;font-weight:700;color:",";"],(function(e){return e.theme.colors.text})),u=i.d.div.withConfig({displayName:"Bio__Description",componentId:"sc-5v8ml6-3"})(["margin-bottom:11.2px;line-height:1.5;font-size:16px;color:",";"],(function(e){return e.theme.colors.secondaryText})),p=i.d.div.withConfig({displayName:"Bio__LinksWrapper",componentId:"sc-5v8ml6-4"})(["& a{margin-right:9.6px;}& svg{width:25.6px;height:25.6px;cursor:pointer;}& svg path{fill:",";transition:fill 0.3s;}& a:hover svg path{fill:",";}"],(function(e){return e.theme.colors.icon}),(function(e){return e.theme.colors.text})),g=function(e){var t=e.link,n=e.children;return t?o.a.createElement("a",{href:t,target:"_blank",rel:"noreferrer"},n):null};t.a=function(){var e=r.links.github,t=r.links.kaggle,n=r.links.instagram,a=r.links.facebook,i=r.links.linkedIn,s=r.links.email,f=r.links.etc;return o.a.createElement(c,{id:"bio"},o.a.createElement(m,null),o.a.createElement("div",null,o.a.createElement(d,null,"@",r.author),o.a.createElement(u,null,r.description),o.a.createElement(p,null,o.a.createElement(g,{link:e},o.a.createElement(l.c,null)),o.a.createElement(g,{link:t},o.a.createElement(l.e,null)),o.a.createElement(g,{link:n},o.a.createElement(l.d,null)),o.a.createElement(g,{link:a},o.a.createElement(l.b,null)),o.a.createElement(g,{link:i},o.a.createElement(l.g,null)),o.a.createElement(g,{link:s},o.a.createElement(l.a,null)),o.a.createElement(g,{link:f},o.a.createElement(l.f,null)))))}}}]);
//# sourceMappingURL=component---src-pages-index-jsx-5c137d51ee6370db6549.js.map
'''
作者: 李展旗
Date: 2023-10-03 16:22:09
文件最后编辑者: 李展旗
LastEditTime: 2023-10-04 19:05:40
'''
"""
视图页面的调用方法
queryset=UserInfo.objects.filter(**data_dict).all().order_by("id") 
pag=paginator.paginator(queryset,request,8)
page_data=pag.get_data(page)
html_data=pag.get_html(page)

模板文件中的方法
<nav aria-label="...">
        <ul class="pagination">

          {{ html_data }}
          <div style="float:right;">
            <form action="" method="get">
                <div class="input-group mb-3">
                    <input type="text" name='page' class="form-control " value="{{page}}" placeholder="页码" aria-label="Recipient's username" aria-describedby="button-addon2">
                    <div class="input-group-append">
                    <button class="btn btn-outline-secondary" type="submit" id="button-addon2">
                        跳转
                    </button>
                    </div>
                </div>
            </form>
        </div>
        </ul>
      </nav>
"""

from django.core.paginator import Paginator
from django.utils.safestring import mark_safe
import copy

class paginator:
    def __init__(self,queryset,request,size):
        #queryset可以是数据库查询结果也可以是列表
        #request是请求对象，需要进行传进来进行处理一下跳转
        #size分页的内容条目的多少
        self.query_dict=copy.deepcopy(request.GET)
        self.query_dict._mutable=True
        self.paginator=Paginator(queryset,per_page=size)
        self.page=request.GET.get('page',"1")
        if self.page.isdecimal():
            self.page=int(self.page)
        else:
            self.page=1
    def get_html(self,page):
        #返回html文件，可以直接在模板中调用直接显示
        html_elem_dangqian="""
        <li class="page-item active" aria-current="page">
        <span class="page-link">{}</span>
        </li>
        """
        html_elem="""
        <li class="page-item">
        <a class="page-link" href="?{}">{}</a>
        </li>
        """
        html_ele_up_down='''
            <li class="page-item {}">
                <a class="page-link" href="?{}">{}</a>
            </li>
            '''
        html_data=""
        start=page-3
        end=page+3

        page_data=self.get_data(page)

        self.query_dict.setlist("page",[1])
        html_data+=html_ele_up_down.format('',self.query_dict.urlencode(),'首页')

        if page_data.has_previous():
            self.query_dict.setlist("page",[page-1])
            html_data+=html_ele_up_down.format('',self.query_dict.urlencode(),'上一页')
        else:
            html_data+=html_ele_up_down.format('disabled',"",'上一页')

        for i in self.paginator.page_range:
            if i==page:
                html_data+=html_elem_dangqian.format(i)
                continue
            if i>=start and i<=end:
                self.query_dict.setlist("page",[i])
                html_data+=html_elem.format(self.query_dict.urlencode(),i)
            if i>end:
                break
        if page_data.has_next():
            self.query_dict.setlist("page",[page+1])
            html_data+=html_ele_up_down.format('',self.query_dict.urlencode(),'下一页')
        else:
            html_data+=html_ele_up_down.format('disabled',"",'下一页')
        
        self.query_dict.setlist("page",[self.paginator.num_pages])
        html_data+=html_ele_up_down.format('',self.query_dict.urlencode(),'尾页')
        html_data=mark_safe(html_data)
        return html_data
    def get_data(self,page):
        #返回数据
        page_data=self.paginator.get_page(page)
        return page_data



    
    

    

    
    
    # print(paginator.num_pages)
    # print(page_data.paginator.count,page_data.number,page_data.has_next() )

    
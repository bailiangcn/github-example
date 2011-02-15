#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com


"""
维护播放列表工具
"""

__revision__ = '0.1'



import  os
import  wx
import  wx.grid             as  gridlib
import  wx.lib.gridmovers   as  gridmovers
import  movielist
from copy import deepcopy

#---------------------------------------------------------------------------
# 文件选择支持的扩展名
wildcard = u"Mpeg 文件(*.mpg)|*.mpg|"     \
           u"Avi 文件 (*.avi)|*.avi|" \
           u"Real 文件 (*.rm)|*.rm|" \
           u"Real 文件 (*.rmvb)|*.rmvb|" \
           u"所有文件(*.*)|*.*"
#---------------------------------------------------------------------------

class CustomDataTable(gridlib.PyGridTableBase):
    '''
    wxpython下的定制表格类
    '''
    def __init__(self,filename,canmove=True):
        '''
        初始化表格数据,filename表示初始化的数据来源
        canmove表示表格各行能否移动
        '''
        gridlib.PyGridTableBase.__init__(self)

        #定义一个影片列表类
        ml = movielist.Mlist(filename)
        self.identifiers = ['name','path']
        self.colLabels = {'name':u'节目名称','path':u'文件存储路径' }
        #行标签显示值
        self.rowLabels = []
        for i in range(len(ml.mlist)):
            self.rowLabels  += [(u'节目' + unicode(str(i+1), 'utf-8'))]
        #实际数据赋值
        self.data = ml.mlist 
    #--------------------------------------------------
    # 实现接口所需的方法

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.identifiers)

    def IsEmptyCell(self, row, col):
        id = self.identifiers[col]
        return not self.data[row][id]

    def GetValue(self, row, col):
        id = self.identifiers[col]
        return self.data[row][id]

    def SetValue(self, row, col, value):
        id = self.identifiers[col]
        self.data[row][id] = value

    #--------------------------------------------------
    # 一些可以选择实现的方法

    # Called when the grid needs to display column labels
    def GetColLabelValue(self, col):
        id = self.identifiers[col]
        return self.colLabels[id]

    # Called when the grid needs to display row labels
    def GetRowLabelValue(self,row):
        return self.rowLabels[row]

    #--------------------------------------------------

    # 重载数据到表格
    def ReloadData(self,filename):
        ml = movielist.Mlist(filename)

        grid = self.GetView()
        if grid:
            numRows=len(self.data)
            self.rowLabels = []
            for i in range(len(ml.mlist)):
                self.rowLabels  += [(u'节目' + unicode(str(i+1), 'utf-8'))]
            self.data = ml.mlist 

            # Notify the grid
            grid.BeginBatch()
            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, 0,numRows 
                    )
            grid.ProcessTableMessage(msg)
            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 
                    len(self.data) )
            grid.ProcessTableMessage(msg)
            grid.EndBatch()

    # 删除所有行
    def DelRows(self):
        grid = self.GetView()
        if grid:
            numRows=len(self.data)
            self.data=[]
            self.rowLabels=[]

            # Notify the grid
            grid.BeginBatch()
            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, 0,numRows 
                    )
            grid.ProcessTableMessage(msg)
            grid.EndBatch()

    # 删除单独行
    def DelRow(self,rowpos):
        grid = self.GetView()
        if grid:
            del self.data[rowpos]
            self.rowLabels=[]
            for i in range(len(self.data)):
                self.rowLabels  += [(u'节目' + unicode(str(i+1), 'utf-8'))]
            # Notify the grid
            grid.BeginBatch()
            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, rowpos,1 )
            grid.ProcessTableMessage(msg)
            grid.EndBatch()

    # 移动行
    def MoveRow(self,frm,to):
        grid = self.GetView()

        if grid:
            # Move the rowLabels and data rows
            oldData = self.data[frm]
            del self.data[frm]
            if to > frm:
                self.data.insert(to-1,oldData)
            else:
                self.data.insert(to,oldData)

            # Notify the grid
            grid.BeginBatch()
            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_INSERTED, to, 1)
            grid.ProcessTableMessage(msg)
            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, frm, 1)
            grid.ProcessTableMessage(msg)
            grid.EndBatch()


#---------------------------------------------------------------------------


class DragableGrid(gridlib.Grid):
    '''
    实际实现的表格与数据绑定
    '''
    def __init__(self, parent,filename,canmove=True):
        '''
        初始化
        filename表示初始化的数据来源
        canmove表示表格各行能否移动
        '''
        gridlib.Grid.__init__(self, parent, -1)
        table = CustomDataTable(filename,canmove)
        # 第二个参数标识覆盖表格数据后自动销毁
        self.SetTable(table, True)
        #自动调整列宽
        self.AutoSizeColumns()
        #禁止调整行高
        self.EnableDragRowSize(False)

        # 如果允许行移动设置绑定
        gridmovers.GridRowMover(self)
        if canmove:
            self.Bind(gridmovers.EVT_GRID_ROW_MOVE, self.OnRowMove, self)
        #设置右键点击标签删除功能的绑定
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, 
                self.OnLabelRightClick)

    def OnLabelRightClick(self, evt):
        '''
        右键点击标签后删除当前行
        '''
        rowpos=evt.GetRow()
        moviestr=self.GetTable().GetValue(rowpos,0)
        dlg = wx.MessageDialog(self, u'是否删除此条节目?\n'+moviestr,
                   u'确认', wx.YES_NO | wx.NO_DEFAULT 
                   | wx.ICON_INFORMATION
                   )
        if dlg.ShowModal() == wx.ID_YES:
            self.GetTable().DelRow(rowpos)
            self.SaveData()
        dlg.Destroy()
        evt.Skip()

    def OnRowMove(self,evt):
        '''
        当行发生移动
        '''
        frm = evt.GetMoveRow()          # Row being moved
        to = evt.GetBeforeRow()         # Before which row to insert
        self.GetTable().MoveRow(frm,to)
        self.SaveData()

    def SaveData(self,filename=u'templist.xml'):
        '''
        保存表格数据到文件
        '''
        ml = movielist.Mlist(empty=True)
        ml.mlist=self.GetTable().data
        ml.savefile(filename)

#----------------------------------------------------------------------
class TabPanel(wx.Panel):
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent)
#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
    '''
    主调用框架
    '''
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, u"节目播出顺序调整", 
                size=(1024,768))
        #设置标签
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)

        tabOne = TabPanel(notebook)
        notebook.AddPage(tabOne, u"轮播节目单调整")
        tabTwo = TabPanel(notebook)
        notebook.AddPage(tabTwo, u"插播节目调整")
        #设置位置容器
        sizer = wx.BoxSizer(wx.VERTICAL)
        tabOne.sizer1 = wx.BoxSizer(wx.VERTICAL)
        tabOne.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        tabOne.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        tabOne.sizer4 = wx.BoxSizer(wx.VERTICAL)
        tabOne.sizer5 = wx.BoxSizer(wx.VERTICAL)
        #定义临时表格
        self.gridnew = DragableGrid(tabOne,u'templist.xml')
        #定义当前应用的表格,只读
        self.gridold = DragableGrid(tabOne,u'mainlist.xml',canmove=False)
        for i in range(self.gridold.GetNumberRows()):
            self.gridold.SetReadOnly(i,0,True)
            self.gridold.SetReadOnly(i,1,True)

        #定义一组文字标签
        font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.st1 = wx.StaticText(tabOne, -1, u"当前服务器播出清单")
        self.st2 = wx.StaticText(tabOne, -1, u"临时操作清单")
        self.st1.SetFont(font)
        self.st2.SetFont(font)

        #定义一组功能按钮
        self.bn1 = wx.Button(tabOne,  -1, u"清空列表")
        self.Bind(wx.EVT_BUTTON, self.OnReset, self.bn1)


        self.bn2 = wx.Button(tabOne, -1, u"读取路径下所有文件")
        self.Bind(wx.EVT_BUTTON, self.OnPickDir, self.bn2)

        self.bn3 = wx.Button(tabOne,  -1, u"退出")
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.bn3)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.bn4 = wx.Button(tabOne, -1, u"上传服务器")
        self.Bind(wx.EVT_BUTTON, self.OnPush, self.bn4)

        self.bn5 = wx.Button(tabOne, -1, u"添加影片文件")
        self.Bind(wx.EVT_BUTTON, self.OnPickFile, self.bn5)

        self.bn6 = wx.Button(tabOne, -1, u"复制当前播出列表")
        self.Bind(wx.EVT_BUTTON, self.OnPull, self.bn6)

        ##将各组件加入位置容器
        tabOne.sizer4.Add(self.st1, 0, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        tabOne.sizer4.Add(self.gridold, 1, flag=wx.EXPAND|wx.ALL, border=0)
        tabOne.sizer5.Add(self.st2, 0, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        tabOne.sizer5.Add(self.gridnew, 1, flag=wx.EXPAND|wx.ALL, border=0)

        tabOne.sizer2.Add(self.bn1, 1, wx.ALIGN_CENTER | wx.ALL, border=5)
        tabOne.sizer2.Add(self.bn6, 1, wx.ALIGN_CENTER | wx.ALL, border=5)
        tabOne.sizer2.Add(self.bn2, 1, wx.ALIGN_CENTER | wx.ALL, border=5)
        tabOne.sizer2.Add(self.bn5, 1, wx.ALIGN_CENTER | wx.ALL, border=5)
        tabOne.sizer2.Add(self.bn4, 1, wx.ALIGN_CENTER | wx.ALL, border=5)
        tabOne.sizer2.Add(self.bn3, 1, wx.ALIGN_CENTER | wx.ALL, border=5)

        tabOne.sizer3.Add(tabOne.sizer4, 1, flag=wx.EXPAND|wx.ALL, border=5)
        tabOne.sizer3.Add(tabOne.sizer5, 1, flag=wx.EXPAND|wx.ALL, border=5)

        tabOne.sizer1.Add(tabOne.sizer3, 1, flag=wx.EXPAND|wx.ALL, border=5)
        tabOne.sizer1.Add(tabOne.sizer2, 0, flag=wx.EXPAND|wx.ALL, border=5)

        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        tabOne.SetSizer(tabOne.sizer1)
        tabOne.Layout()

        #自动调整尺寸、布局
        panel.SetSizer(sizer)
        self.Layout()
        self.Show()


    def OnReset(self, event):
        '''
        清空临时播出列表
        '''
        ml = movielist.Mlist(empty=True)
        ml.savefile('templist.xml')
        self.gridnew.GetTable().DelRows()
        self.gridnew.AutoSizeColumns()

    def OnPush(self, event):
        '''
        上传到实际播出列表
        '''
        ml = movielist.Mlist('templist.xml')
        if ml.length >0:
            ml.savefile('mainlist.xml')
            self.gridold.GetTable().ReloadData('templist.xml')
            self.gridold.AutoSizeColumns()
        
    def OnPull(self, event):
        '''
        复制播出列表
        '''
        mla = movielist.Mlist(u'mainlist.xml')
        mlb = movielist.Mlist(u'templist.xml')
        mlb.mlist.extend(mla.mlist)
        mlb.savefile(u'templist.xml')
        self.gridnew.GetTable().ReloadData(u'templist.xml')
        self.gridnew.AutoSizeColumns()


    def OnPickDir(self, evt):
        '''
        选择文件目录添加影片
        '''
        dlg = wx.DirDialog(self, u"请选择影片所在目录",
                          style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           )
        if dlg.ShowModal() == wx.ID_OK:
            ml = movielist.Mlist(u'templist.xml')
            if sys.getfilesystemencoding() != u'UTF-8':
                #wxpython默认在vim下面无法正常得到有效unicode编码,
                #为方便调试,需要进行转换
                tmppath=repr(dlg.GetPath())[1:]
                exec 'tmppath='+ tmppath
                path=tmppath.decode('utf-8')
            else:
                path=dlg.GetPath()

            ml.makebaselist(path)
            ml.savefile(u'templist.xml')
            self.gridnew.GetTable().ReloadData(u'templist.xml')
            self.gridnew.AutoSizeColumns()
        dlg.Destroy()

    def OnPickFile(self, evt):
        '''
        选择单个影片文件添加
        '''
        dlg = wx.FileDialog(
                    self, message=u"选择影片文件",
                    defaultDir=os.getcwd(), 
                    defaultFile="",
                    wildcard=wildcard,
                    style=wx.OPEN | wx.MULTIPLE
                    )
        if dlg.ShowModal() == wx.ID_OK:
            ml = movielist.Mlist('templist.xml')
            # 选择返回一个多个文件的列表
            paths = dlg.GetPaths()
            for eachfile in paths:
                if sys.getfilesystemencoding() != u'UTF-8':
                    #wxpython默认在vim下面无法正常得到有效unicode编码,
                    #为方便调试,需要进行转换
                    tmpfile = repr(eachfile)[1:]
                    exec 'tmpfile='+ tmpfile
                    path=tmpfile.decode('utf-8')
                else:
                    path=eachfile
                tempmn=os.path.splitext(os.path.basename(path))[0]
                ml.append([tempmn, path])
            ml.savefile(u'templist.xml')
            self.gridnew.GetTable().ReloadData(u'templist.xml')
            self.gridnew.AutoSizeColumns()
        dlg.Destroy()

    def OnCloseMe(self, event):
        '''
        点击关闭按钮
        '''
        self.Close(True)

    def OnCloseWindow(self, event):
        '''
        点击关闭窗口
        '''
        self.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.PySimpleApp()
    frame = TestFrame(None)
    app.MainLoop()

#---------------------------------------------------------------------------

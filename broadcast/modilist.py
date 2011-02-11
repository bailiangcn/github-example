#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com


"""
维护播放列表工具
"""

__revision__ = '0.1'



import  wx
import  wx.grid             as  gridlib
import  wx.lib.gridmovers   as  gridmovers
import movielist

#---------------------------------------------------------------------------

class CustomDataTable(gridlib.PyGridTableBase):
    def __init__(self):
        gridlib.PyGridTableBase.__init__(self)

        ml = movielist.Mlist()
        self.identifiers = ['name','path']
        self.rowLabels = []

        self.colLabels = {'name':u'节目名称','path':u'文件存储路径' }
        for i in range(len(ml.mlist)):
            self.rowLabels  += [(u'节目' + unicode(str(i+1), 'utf-8'))]


        self.data = ml.mlist 

    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface

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
    # Some optional methods

    # Called when the grid needs to display column labels
    def GetColLabelValue(self, col):
        id = self.identifiers[col]
        return self.colLabels[id]

    # Called when the grid needs to display row labels
    def GetRowLabelValue(self,row):
        return self.rowLabels[row]

    #--------------------------------------------------
    # Methods added for demo purposes.

    # The physical moving of the cols/rows is left to the implementer.
    # Because of the dynamic nature of a wxGrid the physical moving of
    # columns differs from implementation to implementation

    # Move the row
    def MoveRow(self,frm,to):
        grid = self.GetView()

        if grid:
            # Move the rowLabels and data rows
            oldLabel = self.rowLabels[frm]
            oldData = self.data[frm]
            del self.rowLabels[frm]
            del self.data[frm]

            if to > frm:
                self.rowLabels.insert(to-1,oldLabel)
                self.data.insert(to-1,oldData)
            else:
                self.rowLabels.insert(to,oldLabel)
                self.data.insert(to,oldData)

            # Notify the grid
            grid.BeginBatch()

            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_INSERTED, to, 1
                    )
            grid.ProcessTableMessage(msg)

            msg = gridlib.GridTableMessage(
                    self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, frm, 1
                    )
            grid.ProcessTableMessage(msg)
    
            grid.EndBatch()


#---------------------------------------------------------------------------


class DragableGrid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)

        table = CustomDataTable()

        # The second parameter means that the grid is to take ownership of the
        # table and will destroy it when done.  Otherwise you would need to keep
        # a reference to it and call it's Destroy method later.
        self.SetTable(table, True)
        self.AutoSizeColumns()

        # Enable Row moving
        gridmovers.GridRowMover(self)
        self.Bind(gridmovers.EVT_GRID_ROW_MOVE, self.OnRowMove, self)


    # Event method called when a row move needs to take place
    def OnRowMove(self,evt):
        frm = evt.GetMoveRow()          # Row being moved
        to = evt.GetBeforeRow()         # Before which row to insert
        self.GetTable().MoveRow(frm,to)

#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, u"节目播出顺序调整", 
                size=(800,600))
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.grid = DragableGrid(self)

        self.bn1 = wx.Button(self,  -1, u"清空列表")
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.bn1)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.bn2 = wx.Button(self,  -1, u"退出")
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.bn2)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.sizer2.Add(self.bn1, 1, wx.ALIGN_CENTER | wx.ALL, border=10)
        self.sizer2.Add(self.bn2, 1, wx.ALIGN_CENTER | wx.ALL, border=10)

        self.sizer1.Add(self.grid, 1, flag=wx.EXPAND|wx.ALL, border=15)
        self.sizer1.Add(self.sizer2, 0, flag=wx.EXPAND|wx.ALL, border=10)
        self.SetSizer(self.sizer1)
        self.SetAutoLayout(1)
        #self.sizer1.Fit(self)

        self.Show()

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.PySimpleApp()
    frame = TestFrame(None)
    #frame.Show(True)
    app.MainLoop()

#---------------------------------------------------------------------------

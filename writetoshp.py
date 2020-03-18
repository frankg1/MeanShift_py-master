# -*- coding: utf-8 -*-
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import os


workspace=os.path.abspath('.')
print(workspace)
def createshp(X,c,c1,name):
    shpname="cs"+str(name)
    #除了weightpoint&pointorignal全部是numpy数组
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")    #gdal处理栅格数据
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    ogr.RegisterAll()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(workspace+'/points')

    if os.access(os.path.join(workspace,shpname+'.shp'), os.F_OK):
        driver.DeleteDataSource(os.path.join(workspace,shpname+'.shp'))


    shapLayer = ds.CreateLayer(shpname, geom_type=ogr.wkbPoint)


    fieldDefn = ogr.FieldDefn('type', ogr.OFTString)
    fieldwidth=20
    #fieldwidth = 100
    fieldDefn.SetWidth(fieldwidth)
    shapLayer.CreateField(fieldDefn)

    fieldDefn = ogr.FieldDefn('typemark', ogr.OFTReal)
    fieldwidth=20
    #fieldwidth = 100
    fieldDefn.SetWidth(fieldwidth)
    shapLayer.CreateField(fieldDefn)

    fieldDefn = ogr.FieldDefn('lon', ogr.OFTString)
    fieldwidth=20
    #fieldwidth = 100
    fieldDefn.SetWidth(fieldwidth)
    shapLayer.CreateField(fieldDefn)

    fieldDefn = ogr.FieldDefn('lat', ogr.OFTString)
    fieldwidth=20
    #fieldwidth = 100
    fieldDefn.SetWidth(fieldwidth)
    shapLayer.CreateField(fieldDefn)

    #line图层也创建一个字段
    fieldDefn = ogr.FieldDefn('remark', ogr.OFTString)
    fieldwidth=20
    #fieldwidth = 100
    fieldDefn.SetWidth(fieldwidth)


   #每一行记录重复一次，就是每一个点的数据
   #X
    for x in X:
        defn = shapLayer.GetLayerDefn()
        feature = ogr.Feature(defn)
        feature.SetField('type','有效栅格' )
        feature.SetField('typemark',x[2] )
        feature.SetField('lon', x[0])
        feature.SetField('lat',x[1] )
        wkt = "POINT(%f %f)" % (x[0], x[1])
        point = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(point)
        shapLayer.CreateFeature(feature)
        feature.Destroy()

    defn = shapLayer.GetLayerDefn()
    feature = ogr.Feature(defn)
    feature.SetField('type','有效栅格' )
    feature.SetField('typemark',1000 )
    feature.SetField('lon', c[0])
    feature.SetField('lat',c[1] )
    wkt = "POINT(%f %f)" % (c[0], c[1])
    point = ogr.CreateGeometryFromWkt(wkt)
    feature.SetGeometry(point)
    shapLayer.CreateFeature(feature)
    feature.Destroy()

    defn = shapLayer.GetLayerDefn()
    feature = ogr.Feature(defn)
    feature.SetField('type','有效栅格' )
    feature.SetField('typemark',1000 )
    feature.SetField('lon', c1[0])
    feature.SetField('lat',c1[1] )
    wkt = "POINT(%f %f)" % (c1[0], c1[1])
    point = ogr.CreateGeometryFromWkt(wkt)
    feature.SetGeometry(point)
    shapLayer.CreateFeature(feature)
    feature.Destroy()


    #最后写完了一个图层文件的结束
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)
    prj_file = os.path.join(workspace, shpname) + ".prj"
    prjFile = open(prj_file, 'w')
    sr.MorphToESRI()
    prjFile.write(sr.ExportToWkt())
    prjFile.close()
    ds.Destroy()
public static class GeoTiffReader
{
  /// <summary>
  /// Creates a profile family based on a template and a PolyCurve
  /// </summary>
  /// <param name="filePath">Path of GEOTiff file</param>
  /// <returns>returns a list of objects with the following fields: latitude, longitude and elevation</returns>
  public static List<Dictionary<string, double>> Read(string filePath)
  {
    using (Tiff tiff = Tiff.Open(filePath, "r"))
    {
      int num1 = tiff.GetField(TiffTag.IMAGELENGTH)[0].ToInt();
      FieldValue[] field1 = tiff.GetField(TiffTag.GEOTIFF_MODELPIXELSCALETAG);
      FieldValue[] field2 = tiff.GetField(TiffTag.GEOTIFF_MODELTIEPOINTTAG);
      byte[] bytes1 = field1[1].GetBytes();
      double num2 = BitConverter.ToDouble(bytes1, 0);
      double num3 = BitConverter.ToDouble(bytes1, 8) * -1.0;
      byte[] bytes2 = field2[1].GetBytes();
      double num4 = BitConverter.ToDouble(bytes2, 24);
      double num5 = BitConverter.ToDouble(bytes2, 32) + num3 / 2.0;
      double num6 = num4 + num2 / 2.0;
      byte[] buffer = new byte[tiff.ScanlineSize()];
      double num7 = num5;
      double num8 = num6;
      List<Dictionary<string, double>> dictionaryList = new List<Dictionary<string, double>>();
      for (int row = 0; row < num1; ++row)
      {
        tiff.ReadScanline(buffer, row);
        double num9 = num7 + num3 * (double) row;
        for (int startIndex = 0; startIndex < buffer.Length; startIndex += 4)
        {
          double num10 = num8 + num2 * (double) startIndex / 4.0;
          float single = BitConverter.ToSingle(buffer, startIndex);
          dictionaryList.Add(new Dictionary<string, double>()
          {
            {
              "latitude",
              num9
            },
            {
              "longitude",
              num10
            },
            {
              "elevation",
              (double) single
            }
          });
        }
      }
      return dictionaryList;
    }
  }
}

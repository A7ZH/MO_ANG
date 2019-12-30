import scala.io.Source
import scala.collection.immutable.HashMap
import java.io._

val cuisineList = 
Source.fromFile("YELP-Crawl-Run-2019-12-28T103701Z.csv", "ISO-8859-1").getLines.drop(1)
      .flatMap(rawTxtLine=>{(rawTxtLine.split(",(?=\\S)"))(2)
                                       .stripPrefix("\"").stripSuffix("\"")
                                       .split(';').map(_.trim)})
      .toList.distinct.sortWith(_ < _)
      .foreach(println)

//val file = "cuisine_map.txt"
//val writer = new BufferedWriter(new FileWriter(file))
//for(c<-cuisineMap)
//  writer.write(c.toString + "\n=================================================================\n")
//writer.close()

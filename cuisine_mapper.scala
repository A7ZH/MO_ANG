import scala.io.Source
import scala.collection.immutable.HashMap
import java.io._

val file = "cuisine_map.txt"
val writer = new BufferedWriter(new FileWriter(file))

val cuisineMap = 
Source.fromFile("YELP-Crawl-Run-2019-12-28T103701Z.csv", "ISO-8859-1").getLines.drop(1)
      .flatMap(rawTxtLine=>{
         val lineSplitArr = rawTxtLine.split(",(?=\\S)");
         val name = lineSplitArr(0).stripPrefix("\"").stripSuffix("\"");
         val addr = lineSplitArr(1).stripPrefix("\"").stripSuffix("\"");
         val cuisine_tags = lineSplitArr(2).stripPrefix("\"").stripSuffix("\"").split(';').map(_.trim);
         cuisine_tags.map(t=>(t,(name, addr)))
       })
      .foldLeft(HashMap[String, List[Tuple2[String,String]]]())(
         (cuisineMapSoFar, nextEntry)=>{
           val cuisine = nextEntry._1;
           val nameAddr = nextEntry._2;
           if(cuisineMapSoFar.contains(cuisine)) 
                cuisineMapSoFar + (cuisine -> (cuisineMapSoFar(cuisine) :+ nameAddr)) 
           else cuisineMapSoFar + (cuisine -> List[(String,String)]((nameAddr)))
         })
for(c<-cuisineMap){
  writer.write(c.toString + "\n" + "=================================================================\n")
}
writer.close()

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class SentimentCount {

    public static class SentimentMapper
            extends Mapper<Object, Text, Text, IntWritable> {

        private final Text sentiment = new Text();
        private final IntWritable one = new IntWritable(1);

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString().trim();

            if (line.equalsIgnoreCase("sentiment,text")) {
                return;
            }

            int comma = line.indexOf(',');
            if (comma < 0) {
                return;
            }

            String label = line.substring(0, comma).trim();

            if (label.equalsIgnoreCase("Positive")
    || label.equalsIgnoreCase("Negative")
    || label.equalsIgnoreCase("Mixed_feelings")
    || label.equalsIgnoreCase("unknown_state")
    || label.equalsIgnoreCase("not-Tamil")) {

                sentiment.set(label);
                context.write(sentiment, one);
            }
        }
    }

    public static class SentimentReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private final IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values,
                           Context context)
                throws IOException, InterruptedException {

            int total = 0;

            for (IntWritable value : values) {
                total += value.get();
            }

            result.set(total);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {

        if (args.length != 2) {
            System.err.println(
                "Usage: SentimentCount <input> <output>");
            System.exit(2);
        }

        Job job = Job.getInstance(
                new Configuration(), "SocialPulse360 Sentiment Count");

        job.setJarByClass(SentimentCount.class);
        job.setMapperClass(SentimentMapper.class);
        job.setCombinerClass(SentimentReducer.class);
        job.setReducerClass(SentimentReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

package com.example.fire_detection_system;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.util.Log;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity {
    HttpURLConnection conn = null;
    TextView currDate = null;
    TextView currTemp = null;
    TextView currHum = null;
    TextView currpre = null;
    TextView temp1 = null;
    TextView temp2 = null;
    TextView hum1 = null;
    TextView hum2 = null;
    TextView pre1 = null;
    TextView pre2 = null;
    TextView time1 = null;
    TextView time2 = null;
    TextView fireProbability=null;


    // SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Date date = new Date();
        currDate = findViewById(R.id.dateText);
        currTemp = findViewById(R.id.dispTemp);
        currHum = findViewById(R.id.humidityText);
        currpre = findViewById(R.id.currpre);

        temp1 = findViewById(R.id.temp1);
        temp2 = findViewById(R.id.temp2);
        hum1 = findViewById(R.id.hum1);
        hum2 = findViewById(R.id.hum2);
        pre1 = findViewById(R.id.pre1);
        pre2 = findViewById(R.id.pre2);
        time1 = findViewById(R.id.time1);
        time2 = findViewById(R.id.time2);

        fireProbability = findViewById(R.id.fireprob);

//      fireProbability.addTextChangedListener(new TextWatcher() {
//          @Override
//          public void beforeTextChanged(CharSequence s, int start, int count, int after) {
//
//          }
//
//          @Override
//          public void onTextChanged(CharSequence s, int start, int before, int count) {
//
//          }
//
//          @Override
//          public void afterTextChanged(Editable s) {
//              checkFire(s.toString());
//
//          }
//      });

        String dateTime = currDateTime();
        currDate.setText(dateTime);
        parseData();

    }
    public void checkFire(String h){

        Log.d("fireprob", h);

        double fireProb = Double.parseDouble(h);
        if(fireProb >= 0.80){
            Intent myIntent = new Intent(MainActivity.this, FireAlert.class);
            myIntent.putExtra("fireprobability", fireProb);
            startActivity(myIntent);
            AlarmManager alarmManager =
                    (AlarmManager) this.getSystemService(Context.ALARM_SERVICE);
            Intent intent = new Intent(MainActivity.this, FireAlert.class);
            PendingIntent pendingIntent = PendingIntent.getBroadcast(this, 0,intent,0);
            alarmManager.setInexactRepeating(AlarmManager.ELAPSED_REALTIME_WAKEUP, SystemClock.elapsedRealtime() + AlarmManager.INTERVAL_HALF_HOUR, AlarmManager.INTERVAL_HALF_HOUR, pendingIntent);

        }

    }

    public String currDateTime(){
            Date date = new Date();
            SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");

            String dateText = formatter.format(date);
            return dateText;
    }

    public void parseData(){
        JSONTask myTask = new JSONTask();
        myTask.execute( "https://api.thingspeak.com/channels/1219334/feeds.json?api_key=N6Z53E97Y26LIYTK&results=2");
    }

    class JSONTask extends AsyncTask<String, String, String>{
        @Override
        protected String doInBackground(String... strings) {
            try{
                URL url = new URL(strings[0]);
                conn = (HttpURLConnection) url.openConnection();
                conn.setReadTimeout(10000);
                conn.connect();

                if(conn.getResponseCode() == HttpURLConnection.HTTP_OK){
                    InputStream inputStream = conn.getInputStream();
                    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
                    StringBuffer stringBuffer = new StringBuffer();
                    String line = "";
                    while((line = bufferedReader.readLine()) != null){
                        stringBuffer.append(line);
                    }
                    return stringBuffer.toString();
                }

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(String s) {

            super.onPostExecute(s);
            String jsonString = s;
            try{
                JSONObject jsonObject = new JSONObject(jsonString);
                JSONArray jsonArray = jsonObject.getJSONArray("feeds");

//                for(int i = 0; i < jsonArray.length(); i++){
//                    JSONObject jsonObject1 = jsonArray.getJSONObject(i);
//                    String timel = jsonObject1.getString("created_at");
//                    String idl = jsonObject1.getString("entry_id");
//                    String templ= jsonObject1.getString("field1");
//                    String pressurel= jsonObject1.getString("field3");
//                    String humidityl= jsonObject1.getString("field2");
//                    String fireprobl= jsonObject1.getString("field4");
//
//
//
//
//                }
                JSONObject firstObj = jsonArray.getJSONObject(1);
                String time = firstObj.getString("created_at");
                String id = firstObj.getString("entry_id");
                String temp= firstObj.getString("field1");
                String pressure= firstObj.getString("field3");
                String humidity= firstObj.getString("field2");
                double fireprob = firstObj.getDouble("field4");

                JSONObject secondObj = jsonArray.getJSONObject(0);
                String time02 = secondObj.getString("created_at");
                String id2 = secondObj.getString("entry_id");
                String temp02= secondObj.getString("field1");
                String pressure2= secondObj.getString("field3");
                String humidity2= secondObj.getString("field2");

                String probstr = String.valueOf(fireprob);
                Handler mHandler = new Handler();
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        while(true){
                            try{
                                Thread.sleep(1000);
                                mHandler.post(new Runnable() {
                                    @Override
                                    public void run() {
                                        currDate.setText(time);
                                        currTemp.setText(temp);
                                        currpre.setText(pressure);
                                        currHum.setText(humidity);
                                        fireProbability.setText(probstr);
                                    }
                                });
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                    }
                }).start();
//                runOnUiThread(new Runnable() {
//                    @Override
//                    public void run() {
//                        try {
//                            Thread.sleep(1000);
//                            currDate.setText(time);
//                            currTemp.setText(temp);
//                            currpre.setText(pressure);
//                            currHum.setText(humidity);
//                            fireProbability.setText(probstr);
//                        } catch (InterruptedException e) {
//                            e.printStackTrace();
//                        }
//
//                    }
//                }).start();

//                currDate.setText(time);
//                currTemp.setText(temp);
//                currpre.setText(pressure);
//                currHum.setText(humidity);
//                fireProbability.setText(probstr);

                time1.setText(time);
                temp1.setText(temp);
                pre1.setText(pressure);
                hum1.setText(humidity);

                time2.setText(time02);
                temp2.setText(temp02);
                pre2.setText(pressure2);
                hum2.setText(humidity2);

            } catch (JSONException e) {
                e.printStackTrace();
            }

        }
    }
}
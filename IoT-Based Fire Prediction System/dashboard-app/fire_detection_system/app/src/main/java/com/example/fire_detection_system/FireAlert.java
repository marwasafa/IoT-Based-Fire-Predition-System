package com.example.fire_detection_system;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

public class FireAlert extends AppCompatActivity {
    double fireProbability;
    TextView fp;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fire_alert);
        fp =(TextView) findViewById(R.id.textView);
        fireProbability = getIntent().getDoubleExtra("fireprobability", 0.00);
        double fprobpercent = fireProbability * 100;
        String msg = "there is a "+ fprobpercent + "% probability of fire";
        fp.setText(msg);









    }

    public void goback(View view) {
        Intent backIntent = new Intent(FireAlert.this, MainActivity.class);
        startActivity(backIntent);
    }
}

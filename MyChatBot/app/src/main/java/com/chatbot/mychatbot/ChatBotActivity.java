package com.chatbot.mychatbot;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.samsao.messageui.views.MessagesWindow;

public class ChatBotActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat_bot);

        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        final MessagesWindow messagesWindow = (MessagesWindow)findViewById(R.id.customized_messages_window);
        final EditText message = messagesWindow.getWritingMessageView().findViewById(R.id.message_box_text_field);

        message.setHint("Type here...");
        messagesWindow.setBackgroundResource(R.color.design_default_color_primary_dark);

        messagesWindow.getWritingMessageView().findViewById(R.id.message_box_button).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                messagesWindow.sendMessage(message.getText().toString());

                //now send and edit text data to python script as argument..
                Python py = Python.getInstance();
                PyObject pyobj = py.getModule("myscript");
                PyObject obj = pyobj.callAttr("main", message.getText().toString());

                //and set obj to receive messages
                messagesWindow.receiveMessage(obj.toString());

                message.setText("");
            }
        });
    }
}
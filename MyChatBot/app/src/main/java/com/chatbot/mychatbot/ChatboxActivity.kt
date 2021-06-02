package com.chatbot.mychatbot

import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity

class ChatboxActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chatbox)
    }

    fun navigateToProfile(view: View) {
        val intent = Intent(this@ChatboxActivity, ProfileActivity::class.java)
        startActivity(intent)
    }
}
package com.chatbot.mychatbot

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.chatbot.mychatbot.databinding.ActivityDashboardBinding

class DashboardActivity : AppCompatActivity() {

    private lateinit var binding: ActivityDashboardBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityDashboardBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnDataPerusahaan.setOnClickListener {
            val intent = Intent(this@DashboardActivity, DataPerusahaanActivity::class.java)
            startActivity(intent)
        }

        binding.btnchatBox.setOnClickListener {
            val intent = Intent(this@DashboardActivity, ChatBotActivity::class.java)
            startActivity(intent)
        }

        binding.btnFormKeuangan.setOnClickListener {
            val intent = Intent(this@DashboardActivity, FormKeuanganActivity::class.java)
            startActivity(intent)
        }

        binding.btnHasilLaporan.setOnClickListener {
            val intent = Intent(this@DashboardActivity, HasilLaporanActivity::class.java)
            startActivity(intent)
        }
    }
}
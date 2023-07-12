using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GUIExampleLab
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button_connect_Click(object sender, EventArgs e)
        {

            string id = textBox_id.Text;
            string pass = textBox_pass.Text;

            if(id == "" || pass == "" )
            {
                button_connect.BackColor = Color.Red;
            }
            else
            {
                button_connect.Enabled = false;
                button_disconnect.Enabled = true;
                button_send.Enabled = true;
                textBox_message.Enabled = true;

                button_connect.BackColor = Color.Green;


            }

        }

        private void button_disconnect_Click(object sender, EventArgs e)
        {
            button_disconnect.Enabled = false;
            button_connect.Enabled = true;
            button_send.Enabled = false;
            textBox_message.Enabled = false;

            button_connect.BackColor = SystemColors.Control;
            button_connect.UseVisualStyleBackColor = true;
        }

        private void button_send_Click(object sender, EventArgs e)
        {

            string id = textBox_id.Text;
            string message = textBox_message.Text;

            richTextBox_output.Text = id + ": " + message + "\n";
            textBox_message.Clear();

        }
    }
}

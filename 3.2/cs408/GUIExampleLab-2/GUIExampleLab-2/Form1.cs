using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GUIExampleLab_2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button_submit_Click(object sender, EventArgs e)
        {
            string message;

            if(checkBox_ice.Checked && checkBox_cake.Checked)
            {
                message = "I like all!";
            }
            else if(checkBox_ice.Checked)
            {
                message = "I like icecream!";
            }
            else if(checkBox_cake.Checked)
            {
                message = "I like cake!";
            }
            else
            {
                message = "I like none of them!";
            }

            richTextBox_out.AppendText(message + "\n");


        }

        private void button_clear_Click(object sender, EventArgs e)
        {
            richTextBox_out.Clear();
        }
    }
}

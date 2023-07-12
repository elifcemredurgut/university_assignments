using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GUIExampleLab_3
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button_submit_Click(object sender, EventArgs e)
        {
            string age;
            string gender;

            if(radioButton_less.Checked)
            {
                age = "child";
            }
            else if(radioButton_between.Checked)
            {
                age = "adult";
            }
            else
            {
                age = "old";
            }

            if(radioButton_female.Checked)
            {
                gender = "female";
            }
            else
            {
                gender = "male";
            }

            richTextBox_out.AppendText("This is a/an " + age + " " + gender + "\n");

        }
 
    }
}

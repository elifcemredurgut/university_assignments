using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GUIExampleLab_4
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button_add_Click(object sender, EventArgs e)
        {

            string fruit = textBox_add.Text;
            listView.Items.Add(fruit);
            textBox_add.Clear();

        }

        private void button_remove_Click(object sender, EventArgs e)
        {
            string to_be_removed = textBox_remove.Text;

            foreach(ListViewItem item in listView.Items)
            {
                if (item.Text == to_be_removed) {
                    listView.Items.Remove(item);
                    break;
                }
            }

            textBox_remove.Clear();

        }
    }
}

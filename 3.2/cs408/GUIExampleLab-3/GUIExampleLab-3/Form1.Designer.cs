namespace GUIExampleLab_3
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.radioButton_less = new System.Windows.Forms.RadioButton();
            this.radioButton_between = new System.Windows.Forms.RadioButton();
            this.radioButton_greater = new System.Windows.Forms.RadioButton();
            this.radioButton_female = new System.Windows.Forms.RadioButton();
            this.radioButton_male = new System.Windows.Forms.RadioButton();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.richTextBox_out = new System.Windows.Forms.RichTextBox();
            this.button_submit = new System.Windows.Forms.Button();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.SuspendLayout();
            // 
            // radioButton_less
            // 
            this.radioButton_less.AutoSize = true;
            this.radioButton_less.Location = new System.Drawing.Point(51, 43);
            this.radioButton_less.Name = "radioButton_less";
            this.radioButton_less.Size = new System.Drawing.Size(160, 29);
            this.radioButton_less.TabIndex = 0;
            this.radioButton_less.TabStop = true;
            this.radioButton_less.Text = "less than 18";
            this.radioButton_less.UseVisualStyleBackColor = true;
            // 
            // radioButton_between
            // 
            this.radioButton_between.AutoSize = true;
            this.radioButton_between.Location = new System.Drawing.Point(51, 99);
            this.radioButton_between.Name = "radioButton_between";
            this.radioButton_between.Size = new System.Drawing.Size(187, 29);
            this.radioButton_between.TabIndex = 1;
            this.radioButton_between.TabStop = true;
            this.radioButton_between.Text = "Between 18-35";
            this.radioButton_between.UseVisualStyleBackColor = true;
            // 
            // radioButton_greater
            // 
            this.radioButton_greater.AutoSize = true;
            this.radioButton_greater.Location = new System.Drawing.Point(51, 152);
            this.radioButton_greater.Name = "radioButton_greater";
            this.radioButton_greater.Size = new System.Drawing.Size(189, 29);
            this.radioButton_greater.TabIndex = 2;
            this.radioButton_greater.TabStop = true;
            this.radioButton_greater.Text = "greater than 35";
            this.radioButton_greater.UseVisualStyleBackColor = true;
            // 
            // radioButton_female
            // 
            this.radioButton_female.AutoSize = true;
            this.radioButton_female.Location = new System.Drawing.Point(51, 57);
            this.radioButton_female.Name = "radioButton_female";
            this.radioButton_female.Size = new System.Drawing.Size(107, 29);
            this.radioButton_female.TabIndex = 3;
            this.radioButton_female.TabStop = true;
            this.radioButton_female.Text = "female";
            this.radioButton_female.UseVisualStyleBackColor = true;
            // 
            // radioButton_male
            // 
            this.radioButton_male.AutoSize = true;
            this.radioButton_male.Location = new System.Drawing.Point(51, 126);
            this.radioButton_male.Name = "radioButton_male";
            this.radioButton_male.Size = new System.Drawing.Size(89, 29);
            this.radioButton_male.TabIndex = 4;
            this.radioButton_male.TabStop = true;
            this.radioButton_male.Text = "male";
            this.radioButton_male.UseVisualStyleBackColor = true;
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.radioButton_less);
            this.groupBox1.Controls.Add(this.radioButton_between);
            this.groupBox1.Controls.Add(this.radioButton_greater);
            this.groupBox1.Location = new System.Drawing.Point(104, 24);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(282, 214);
            this.groupBox1.TabIndex = 5;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Age";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.radioButton_female);
            this.groupBox2.Controls.Add(this.radioButton_male);
            this.groupBox2.Location = new System.Drawing.Point(104, 271);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(282, 186);
            this.groupBox2.TabIndex = 6;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Gender";
            // 
            // richTextBox_out
            // 
            this.richTextBox_out.Location = new System.Drawing.Point(104, 491);
            this.richTextBox_out.Name = "richTextBox_out";
            this.richTextBox_out.Size = new System.Drawing.Size(282, 111);
            this.richTextBox_out.TabIndex = 7;
            this.richTextBox_out.Text = "";
            // 
            // button_submit
            // 
            this.button_submit.Location = new System.Drawing.Point(425, 491);
            this.button_submit.Name = "button_submit";
            this.button_submit.Size = new System.Drawing.Size(133, 47);
            this.button_submit.TabIndex = 8;
            this.button_submit.Text = "submit";
            this.button_submit.UseVisualStyleBackColor = true;
            this.button_submit.Click += new System.EventHandler(this.button_submit_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(12F, 25F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(720, 666);
            this.Controls.Add(this.button_submit);
            this.Controls.Add(this.richTextBox_out);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.RadioButton radioButton_less;
        private System.Windows.Forms.RadioButton radioButton_between;
        private System.Windows.Forms.RadioButton radioButton_greater;
        private System.Windows.Forms.RadioButton radioButton_female;
        private System.Windows.Forms.RadioButton radioButton_male;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.RichTextBox richTextBox_out;
        private System.Windows.Forms.Button button_submit;
    }
}


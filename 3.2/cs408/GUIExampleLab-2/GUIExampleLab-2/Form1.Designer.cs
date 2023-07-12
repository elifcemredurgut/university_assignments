namespace GUIExampleLab_2
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
            this.checkBox_ice = new System.Windows.Forms.CheckBox();
            this.checkBox_cake = new System.Windows.Forms.CheckBox();
            this.richTextBox_out = new System.Windows.Forms.RichTextBox();
            this.button_submit = new System.Windows.Forms.Button();
            this.button_clear = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // checkBox_ice
            // 
            this.checkBox_ice.AutoSize = true;
            this.checkBox_ice.Location = new System.Drawing.Point(109, 95);
            this.checkBox_ice.Name = "checkBox_ice";
            this.checkBox_ice.Size = new System.Drawing.Size(189, 29);
            this.checkBox_ice.TabIndex = 0;
            this.checkBox_ice.Text = "Like Icecream?";
            this.checkBox_ice.UseVisualStyleBackColor = true;
            // 
            // checkBox_cake
            // 
            this.checkBox_cake.AutoSize = true;
            this.checkBox_cake.Location = new System.Drawing.Point(109, 159);
            this.checkBox_cake.Name = "checkBox_cake";
            this.checkBox_cake.Size = new System.Drawing.Size(152, 29);
            this.checkBox_cake.TabIndex = 1;
            this.checkBox_cake.Text = "Like Cake?";
            this.checkBox_cake.UseVisualStyleBackColor = true;
            // 
            // richTextBox_out
            // 
            this.richTextBox_out.Location = new System.Drawing.Point(109, 321);
            this.richTextBox_out.Name = "richTextBox_out";
            this.richTextBox_out.ReadOnly = true;
            this.richTextBox_out.Size = new System.Drawing.Size(272, 114);
            this.richTextBox_out.TabIndex = 2;
            this.richTextBox_out.Text = "";
            // 
            // button_submit
            // 
            this.button_submit.Location = new System.Drawing.Point(109, 244);
            this.button_submit.Name = "button_submit";
            this.button_submit.Size = new System.Drawing.Size(127, 43);
            this.button_submit.TabIndex = 3;
            this.button_submit.Text = "Submit";
            this.button_submit.UseVisualStyleBackColor = true;
            this.button_submit.Click += new System.EventHandler(this.button_submit_Click);
            // 
            // button_clear
            // 
            this.button_clear.Location = new System.Drawing.Point(278, 244);
            this.button_clear.Name = "button_clear";
            this.button_clear.Size = new System.Drawing.Size(103, 43);
            this.button_clear.TabIndex = 4;
            this.button_clear.Text = "Clear";
            this.button_clear.UseVisualStyleBackColor = true;
            this.button_clear.Click += new System.EventHandler(this.button_clear_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(12F, 25F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(543, 499);
            this.Controls.Add(this.button_clear);
            this.Controls.Add(this.button_submit);
            this.Controls.Add(this.richTextBox_out);
            this.Controls.Add(this.checkBox_cake);
            this.Controls.Add(this.checkBox_ice);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.CheckBox checkBox_ice;
        private System.Windows.Forms.CheckBox checkBox_cake;
        private System.Windows.Forms.RichTextBox richTextBox_out;
        private System.Windows.Forms.Button button_submit;
        private System.Windows.Forms.Button button_clear;
    }
}


namespace GUIExampleLab_4
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
            this.textBox_add = new System.Windows.Forms.TextBox();
            this.button_add = new System.Windows.Forms.Button();
            this.listView = new System.Windows.Forms.ListView();
            this.textBox_remove = new System.Windows.Forms.TextBox();
            this.button_remove = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // textBox_add
            // 
            this.textBox_add.Location = new System.Drawing.Point(84, 81);
            this.textBox_add.Name = "textBox_add";
            this.textBox_add.Size = new System.Drawing.Size(197, 31);
            this.textBox_add.TabIndex = 0;
            // 
            // button_add
            // 
            this.button_add.Location = new System.Drawing.Point(313, 75);
            this.button_add.Name = "button_add";
            this.button_add.Size = new System.Drawing.Size(165, 43);
            this.button_add.TabIndex = 1;
            this.button_add.Text = "Add";
            this.button_add.UseVisualStyleBackColor = true;
            this.button_add.Click += new System.EventHandler(this.button_add_Click);
            // 
            // listView
            // 
            this.listView.Location = new System.Drawing.Point(84, 147);
            this.listView.Name = "listView";
            this.listView.Size = new System.Drawing.Size(411, 164);
            this.listView.TabIndex = 2;
            this.listView.UseCompatibleStateImageBehavior = false;
            // 
            // textBox_remove
            // 
            this.textBox_remove.Location = new System.Drawing.Point(84, 344);
            this.textBox_remove.Name = "textBox_remove";
            this.textBox_remove.Size = new System.Drawing.Size(197, 31);
            this.textBox_remove.TabIndex = 3;
            // 
            // button_remove
            // 
            this.button_remove.Location = new System.Drawing.Point(313, 336);
            this.button_remove.Name = "button_remove";
            this.button_remove.Size = new System.Drawing.Size(165, 46);
            this.button_remove.TabIndex = 4;
            this.button_remove.Text = "Remove";
            this.button_remove.UseVisualStyleBackColor = true;
            this.button_remove.Click += new System.EventHandler(this.button_remove_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(12F, 25F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(680, 438);
            this.Controls.Add(this.button_remove);
            this.Controls.Add(this.textBox_remove);
            this.Controls.Add(this.listView);
            this.Controls.Add(this.button_add);
            this.Controls.Add(this.textBox_add);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBox_add;
        private System.Windows.Forms.Button button_add;
        private System.Windows.Forms.ListView listView;
        private System.Windows.Forms.TextBox textBox_remove;
        private System.Windows.Forms.Button button_remove;
    }
}


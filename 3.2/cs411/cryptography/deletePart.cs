logs.AppendText(DateTime.Now + " " + username + " requested to delete a sweet.\n");

string IDToDelete = request.Substring(request.IndexOf("-") + 1);

var lines = File.ReadLines(@sweetsDb);
int lineNum = 0;
string sweet_feed = "";

bool toDelete = false;
bool notOwner = false;

foreach (var line in lines)
{
    if (lineNum > 0)
    {

        string usernameData = line.Substring(0, line.IndexOf(" "));
        string substring_line = line.Substring(line.IndexOf(" ") + 1);
        string sweet_id = substring_line.Substring(0, substring_line.IndexOf(" "));
        string substring_line2 = substring_line.Substring(substring_line.IndexOf(" ") + 1);

        if (sweet_id == IDToDelete && username == usernameData) 
        {
            toDelete = true;
        }
        else
        {
            if (sweet_id == IDToDelete && username != usernameData)
            {
                notOwner = true;

                Byte[] userlistBuffer = Encoding.Default.GetBytes("ERRORThis sweet does not belong to you!");
                try
                {

                    thisClient.Send(userlistBuffer);
                    logs.AppendText(DateTime.Now + " " + username + " tried to delete someone's sweet.\n");
                }
                catch
                {
                    Console.WriteLine("Problem sending ownership error!");
                }
            }
            sweet_feed += usernameData + " " + sweet_id + " " + substring_line2+ "\n";  
        }


    }
    lineNum++;
}
if (toDelete)
{
    System.IO.File.WriteAllText(@sweetsDb, "SWEET DATABASE\n"+sweet_feed);
    Byte[] userlistBuffer = Encoding.Default.GetBytes("ERRORYour sweet is deleted!");
    try
    {

        thisClient.Send(userlistBuffer);
        logs.AppendText(DateTime.Now + " " + username + " delete is successful.\n");
    }
    catch
    {
        Console.WriteLine("Problem sending successful delete!");
    }
}
else if (!notOwner)
{
    Byte[] userlistBuffer = Encoding.Default.GetBytes("ERRORThere is no such sweet!");
    try
    {

        thisClient.Send(userlistBuffer);
        logs.AppendText(DateTime.Now + " " + username + " there is no such sweet.\n");
    }
    catch
    {
        Console.WriteLine("Problem sending invalid delete id!");
    }
}
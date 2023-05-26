using System.Data.SqlTypes;

namespace VivPiSharp;

public class Actions
{
    private bool IsDuringDay()
    {
        return true;
    }

    public bool VerifyTemperature()
    {
        return true;
    }

    public bool VerifyHumidity()
    {
        return true;
    }

    public bool VerifyMisterOrFogger()
    {
        return true;
    }


    public bool ValidateTemperatures()
    {
        return false;
    }

    public bool ValidateHumidity()
    {
        return false;
    }
}
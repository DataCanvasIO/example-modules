package com.zetdata.udf;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

/**
 * Unit test for ExtractSite
 */
public class TestExtractSite
    extends TestCase
{
    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public TestExtractSite( String testName )
    {
        super( testName );
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite()
    {
        return new TestSuite( TestExtractSite.class );
    }

    /**
     * Rigourous Test :-)
     */
    public void testExtractSite()
    {
        assertTrue( true );
    }
}

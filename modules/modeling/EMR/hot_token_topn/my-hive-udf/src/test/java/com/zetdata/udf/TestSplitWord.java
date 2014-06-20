package com.zetdata.udf;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

/**
 * Unit test for SplitWord
 */
public class TestSplitWord
    extends TestCase
{
    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public TestSplitWord( String testName )
    {
        super( testName );
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite()
    {
        return new TestSuite( TestSplitWord.class );
    }

    /**
     * Rigourous Test :-)
     */
    public void testSplitWord()
    {
        assertTrue( true );
    }
}

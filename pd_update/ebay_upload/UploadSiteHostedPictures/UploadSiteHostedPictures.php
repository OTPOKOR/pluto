<?php
/*  ?2013 eBay Inc., All Rights Reserved */ 
/* Licensed under CDDL 1.0 -  http://opensource.org/licenses/cddl1.php */
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<TITLE>UploadSiteHostedPictures</TITLE>
</HEAD>
<BODY>

<?php    
    // These production keys can be obtained by registering at http://developer.ebay.com
    $devID = '5c1e67fb-d674-4784-bbf5-0ebfe79fc96c';
    $appID = 'productv-productv-PRD-ed6845fe4-5ef952a1';
    $certID = 'PRD-d6845fe468d7-47ba-476f-8087-db6f';

    $a = str_replace('$','^',$argv[1]);
    $b = $argv[2];
    $c = $argv[3];

    $d = 'v^1.1#i^1#I^3#p^3#r^0#f^0#t^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'; 
    $e = 'D:/DB/IMG/N225AHA560099/0.jpg'; 
    $f = 'N225AHA560099';
    //the token representing the eBay user to assign the call with
    $userToken = $a;

    $siteID  = 0;                            // siteID needed in request - US=0, UK=3, DE=77...
    $verb    = 'UploadSiteHostedPictures';   // the call being made:
    $version = 517;                          // eBay API version
    
    $file      = $b;       // image file to read and upload
    $picNameIn = $c;
    $handle = fopen($file,'r');         // do a binary read of image
    $multiPartImageData = fread($handle,filesize($file));
    fclose($handle);

    ///Build the request XML request which is first part of multi-part POST
    $xmlReq = '<?xml version="1.0" encoding="utf-8"?>' . "\n";
    $xmlReq .= '<' . $verb . 'Request xmlns="urn:ebay:apis:eBLBaseComponents">' . "\n";
    $xmlReq .= "<Version>$version</Version>\n";
    $xmlReq .= "<PictureName>$picNameIn</PictureName>\n";    
    $xmlReq .= "<RequesterCredentials><eBayAuthToken>$userToken</eBayAuthToken></RequesterCredentials>\n";
    $xmlReq .= '</' . $verb . 'Request>';

    $boundary = "MIME_boundary";
    $CRLF = "\r\n";
    
    // The complete POST consists of an XML request plus the binary image separated by boundaries
    $firstPart   = '';
    $firstPart  .= "--" . $boundary . $CRLF;
    $firstPart  .= 'Content-Disposition: form-data; name="XML Payload"' . $CRLF;
    $firstPart  .= 'Content-Type: text/xml;charset=utf-8' . $CRLF . $CRLF;
    $firstPart  .= $xmlReq;
    $firstPart  .= $CRLF;
    
    $secondPart = '';
    $secondPart .= "--" . $boundary . $CRLF;
    $secondPart .= 'Content-Disposition: form-data; name="dummy"; filename="dummy"' . $CRLF;
    $secondPart .= "Content-Transfer-Encoding: binary" . $CRLF;
    $secondPart .= "Content-Type: application/octet-stream" . $CRLF . $CRLF;
    $secondPart .= $multiPartImageData;
    $secondPart .= $CRLF;
    $secondPart .= "--" . $boundary . "--" . $CRLF;
    
    $fullPost = $firstPart . $secondPart;
    
    // Create a new eBay session (defined below) 
    $session = new eBaySession($userToken, $devID, $appID, $certID, false, $version, $siteID, $verb, $boundary);

    $respXmlStr = $session->sendHttpRequest($fullPost);   // send multi-part request and get string XML response
    if(stristr($respXmlStr, 'HTTP 404') || $respXmlStr == '')
        die('<P>Error sending request');
        
    $respXmlObj = simplexml_load_string($respXmlStr);     // create SimpleXML object from string for easier parsing
                                                          // need SimpleXML library loaded for this
    /* Returned XML is of form 
      <?xml version="1.0" encoding="utf-8"?>
      <UploadSiteHostedPicturesResponse xmlns="urn:ebay:apis:eBLBaseComponents">
        <Timestamp>2007-06-19T16:53:50.370Z</Timestamp>
        <Ack>Success</Ack>
        <Version>517</Version>
        <Build>e517_core_Bundled_4784308_R1</Build>
        <PictureSystemVersion>2</PictureSystemVersion>
        <SiteHostedPictureDetails>
          <PictureName>my_pic</PictureName>
          <PictureSet>Standard</PictureSet>
          <PictureFormat>JPG</PictureFormat>
          <FullURL>http://i21.ebayimg.com/06/i/000/a5/e9/0e60_1.JPG?set_id=7</FullURL>
          <BaseURL>http://i21.ebayimg.com/06/i/000/a5/e9/0e60_</BaseURL>
          <PictureSetMember>...</PictureSetMember>
          <PictureSetMember>...</PictureSetMember>
          <PictureSetMember>...</PictureSetMember>
        </SiteHostedPictureDetails>
      </UploadSiteHostedPicturesResponse>
    */
    
    $ack        = $respXmlObj->Ack;
    $picNameOut = $respXmlObj->SiteHostedPictureDetails->PictureName;
    $picURL     = $respXmlObj->SiteHostedPictureDetails->FullURL;
    
    // print "<P>Picture Upload Outcome : $ack </P>\n";
    // print "<P>picNameOut = $picNameOut </P>\n";
    // print "<P>picURL = $picURL</P>\n";
    // print "<IMG SRC=\"$picURL\">";
    $save =  (string)$picURL;
    print $save;
?>
</BODY>
</HTML>


<?php
// This is a modified version of the 'eBaySession' class which is used in many
// of the other PHP samples.  This has been modified to accomodate multi-part HttpRequests
class eBaySession
{
	private $requestToken;
	private $devID;
	private $appID;
	private $certID;
	private $serverUrl;
	private $compatLevel;
	private $siteID;
	private $verb;
    private $boundary;

	public function __construct($userRequestToken, $developerID, $applicationID, $certificateID, $useTestServer,
								$compatabilityLevel, $siteToUseID, $callName, $boundary)
	{
	    $this->requestToken = $userRequestToken;
	    $this->devID = $developerID;
            $this->appID = $applicationID;
	    $this->certID = $certificateID;
	    $this->compatLevel = $compatabilityLevel;
	    $this->siteID = $siteToUseID;
	    $this->verb = $callName;
            $this->boundary = $boundary;
	    if(!$useTestServer)
		$this->serverUrl = 'https://api.ebay.com/ws/api.dll';
	    else
	        $this->serverUrl = 'https://api.sandbox.ebay.com/ws/api.dll';
	}
	
	/**	sendHttpRequest
		Sends a HTTP request to the server for this session
		Input:	$requestBody
		Output:	The HTTP Response as a String
	*/
	public function sendHttpRequest($requestBody)
	{        
        $headers = array (
            'Content-Type: multipart/form-data; boundary=' . $this->boundary,
            'Content-Length: ' . strlen($requestBody),
	    'X-EBAY-API-COMPATIBILITY-LEVEL: ' . $this->compatLevel,  // API version
			
	    'X-EBAY-API-DEV-NAME: ' . $this->devID,     //set the keys
	    'X-EBAY-API-APP-NAME: ' . $this->appID,
	    'X-EBAY-API-CERT-NAME: ' . $this->certID,

            'X-EBAY-API-CALL-NAME: ' . $this->verb,		// call to make	
	    'X-EBAY-API-SITEID: ' . $this->siteID,      // US = 0, DE = 77...
        );
	//initialize a CURL session - need CURL library enabled
	$connection = curl_init();
	curl_setopt($connection, CURLOPT_URL, $this->serverUrl);
        curl_setopt($connection, CURLOPT_TIMEOUT, 30 );
	curl_setopt($connection, CURLOPT_SSL_VERIFYPEER, 0);
	curl_setopt($connection, CURLOPT_SSL_VERIFYHOST, 0);
	curl_setopt($connection, CURLOPT_HTTPHEADER, $headers);
	curl_setopt($connection, CURLOPT_POST, 1);
	curl_setopt($connection, CURLOPT_POSTFIELDS, $requestBody);
	curl_setopt($connection, CURLOPT_RETURNTRANSFER, 1); 
        curl_setopt($connection, CURLOPT_FAILONERROR, 0 );
        curl_setopt($connection, CURLOPT_FOLLOWLOCATION, 1 );
        //curl_setopt($connection, CURLOPT_HEADER, 1 );           // Uncomment these for debugging
        //curl_setopt($connection, CURLOPT_VERBOSE, true);        // Display communication with serve
        curl_setopt($connection, CURLOPT_USERAGENT, 'ebatns;xmlstyle;1.0' );
        curl_setopt($connection, CURLOPT_HTTP_VERSION, 1 );       // HTTP version must be 1.0
	$response = curl_exec($connection);
        
        if ( !$response ) {
            print "curl error " . curl_errno($connection ) . "\n";
        }
	curl_close($connection);
	return $response;
    } // function sendHttpRequest
}  // class eBaySession
  
    
?>

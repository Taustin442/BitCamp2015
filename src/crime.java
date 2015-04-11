
public class crime {
	 public crime() {
	    }
	 	private int crimeLat;
	 	private int crimeLong;
	 	private int sketch;
	    /**
	     * Will create a BST imperative on order of elements in the array
	     */
	    public crime(int Latitude, int longitude, int sketchyValue) {
	    	crimeLat = Latitude;
	    	crimeLong = longitude;
	    	sketch = sketchyValue;
	    }
	    public int getLat(){
	    	return crimeLat;
	    }
	    public int getLong(){
	    	return crimeLong;
	    }
	    public int getSketch(){
	    	return sketch;
	    }
	    public boolean isLessThan(crime RHS){
	    	return sketch < RHS.getSketch();
	    }
}

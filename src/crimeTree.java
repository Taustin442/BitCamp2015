import java.util.*;

public class crimeTree {

    private TreeNode root;

    public crimeTree() {
    }

    /**
     * Will create a BST imperative on order of elements in the array
     */
    public crimeTree(int[] a) {
    	/* TODO constructor
        this();
        for (int i : a) {
            add(i);
        }
        */
    }

    private static class TreeNode {
        TreeNode left;
        crime item;
        TreeNode right;

        TreeNode(TreeNode left, crime item, TreeNode right) {
            this.left = left;
            this.right = right;
            this.item = item; 
        }
    }

    public void add(crime item) {
        if (root == null) {
            root = new TreeNode(null, item, null);
            return;
        }

        TreeNode node = root;
        while (true) {
            if (item.isLessThan(node.item)) {
                if (node.left == null) {
                    node.left = new TreeNode(null, item, null);
                    break;
                }
                node = node.left;
            } else {
                if (node.right == null) {
                    node.right = new TreeNode(null, item, null);
                    break;
                }
                node = node.right;
            }
        }
    }
    
    public int searchNearby(int currentLat, int currentLon, int range){
    	/*
    	List<crime> nearby = new ArrayList<crime>();
    	return nearby;
    	*/
    	int maxLat = currentLat + range;
    	int maxLon = currentLon + range;
    	int minLat = currentLat - range;
    	int minLon = currentLon - range;
    	List<crime> nearby = new ArrayList<crime>();
    	
    	if(root.item.getLat() > maxLat){
    		nearby.addAll(searchNearbyAux(maxLat, maxLon, root.left, nearby));
    		
    	}
    	else{
    		nearby.add(root.item);
    		nearby.addAll(searchRangeAux(maxLat, minLat, root.left, nearby));
    		nearby.addAll(searchNearbyAux(maxLat, minLat, root.right, nearby));
    	}
    	int sketch = 0;
    	for(int i = 0; i < nearby.size(); i++){
    		crime possible = nearby.get(i);
    		if(possible.getLong() > minLon && possible.getLong() < maxLon){
    			sketch += possible.getLong();
    		}
    	}
    	return sketch;
    }

	private List<crime> searchRangeAux(int maxLat, int minLat, TreeNode node, 
			List<crime> nearby) {
		if(node.item.getLat() < minLat){
			return new ArrayList<crime>();
		}
		else{
			nearby.add(node.item);
			nearby.addAll(searchRangeAux(maxLat, minLat, node.left, nearby));
			nearby.addAll(searchNearbyAux(maxLat, minLat, root.right, nearby));
			return nearby;
		}
	}

	private List<crime> searchNearbyAux(int maxLat, int maxLon, TreeNode node, List<crime> nearby) {
		if(node.item.getLat() > maxLat){
			nearby.addAll(searchNearbyAux(maxLat, maxLon, node.left, nearby));
    		return nearby;
    	}
    	else{
    		nearby.add(node.item);
    		nearby.addAll(searchRangeAux(maxLat, maxLon, node.left, nearby));
    		nearby.addAll(searchNearbyAux(maxLat, maxLon, node.right, nearby));
    		return nearby;
    	}
	}

	
}
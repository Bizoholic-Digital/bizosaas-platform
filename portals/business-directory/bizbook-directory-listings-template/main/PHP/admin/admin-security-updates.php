<?php
include "header.php";
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Security and Updates</span>
                <div class="ud-cen-s2">
                    <h2>Security and updates notifications</h2>
                     <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Topic</th>
									<th>View</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllSecurity() as $row) {

                                ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $row['security_info']; ?>
                                        <span><?php echo dateFormatconverter($row['security_date']); ?></span></td>
                                    <td><a href="<?php echo $row['security_link']; ?>" class="db-list-ststus"
                                           target="_blank">View</a></td>
                                </tr>
                                <?php
                                $si++;
                            }
                            ?>
							</tbody>
						</table>
                    <div class="ud-notes">
                        <p><b>Notes:</b> This window you can get <b>security and update</b> notification from rn53themes.net. This will helpful and stay away from warm attacks and other security threats.</p>
                    </div>
                </div>

            </div>
            </div>
        </div>
    </section>
    <!-- END -->    

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="../js/jquery.min.js"></script>
    <script src="../js/popper.min.js"></script>
    <script src="../js/bootstrap.min.js"></script>
    <script src="../js/jquery-ui.js"></script>
    <script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>